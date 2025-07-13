"""Support for Philips AirPurifier with CoAP."""

from __future__ import annotations

import asyncio
from functools import partial
from ipaddress import IPv6Address, ip_address
import json
import logging
from os import walk
from pathlib import Path

from aioairctrl import CoAPClient
from getmac import get_mac_address

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.http.view import HomeAssistantView
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from homeassistant.helpers.device_registry import format_mac

from .config_entry_data import ConfigEntryData
from .const import (
    CONF_DEVICE_ID,
    CONF_MODEL,
    CONF_STATUS,
    DOMAIN,
    ICONLIST_URL,
    ICONS_PATH,
    ICONS_URL,
    LOADER_PATH,
    LOADER_URL,
    PAP,
    PhilipsApi,
)
from .coordinator import Coordinator
from .model import DeviceInformation
from .philips import model_to_class

_LOGGER = logging.getLogger(__name__)


PLATFORMS = [
    "binary_sensor",
    "button",
    "climate",
    "fan",
    "humidifier",
    "light",
    "number",
    "select",
    "sensor",
    "switch",
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


# icons code thanks to Thomas Loven:
# https://github.com/thomasloven/hass-fontawesome/blob/master/custom_components/fontawesome/__init__.py


class ListingView(HomeAssistantView):
    """Provide a json list of the used icons."""

    requires_auth = False

    def __init__(self, url, iconpath) -> None:
        """Initialize the ListingView with a URL and icon path."""
        self.url = url
        self.iconpath = iconpath
        self.name = "Icon Listing"

    async def get(self, request, *args):
        """Call executor to avoid blocking I/O call to get list of used icons."""
        return await self.hass.async_add_executor_job(
            self.get_icons_list, self.iconpath
        )

    def get_icons_list(self, iconpath):
        """Handle GET request to provide a JSON list of the used icons."""
        icons = []
        for dirpath, _dirnames, filenames in walk(iconpath):
            icons.extend(
                [
                    {"name": (Path(dirpath[len(self.iconpath) :]) / fn[:-4]).as_posix()}
                    for fn in filenames
                    if fn.endswith(".svg")
                ]
            )
        return json.dumps(icons)


async def async_setup(hass: HomeAssistant, config) -> bool:
    """Set up the icons for the Philips AirPurifier integration."""
    _LOGGER.debug("async_setup called")

    await hass.http.async_register_static_paths(
        [StaticPathConfig(LOADER_URL, hass.config.path(LOADER_PATH), True)]
    )
    add_extra_js_url(hass, LOADER_URL)

    iset = PAP
    iconpath = hass.config.path(ICONS_PATH + "/" + iset)
    await hass.http.async_register_static_paths(
        [StaticPathConfig(ICONS_URL + "/" + iset, iconpath, True)]
    )
    hass.http.register_view(ListingView(ICONLIST_URL + "/" + iset, iconpath))

    return True


async def async_get_mac_address_from_host(hass: HomeAssistant, host: str) -> str | None:
    """Get mac address from host."""
    mac_address: str | None

    # first we try if this is an ip address
    try:
        ip_addr = ip_address(host)
    except ValueError:
        # that didn't work, so try a hostname
        mac_address = await hass.async_add_executor_job(
            partial(get_mac_address, hostname=host)
        )
    else:
        # it is an ip address, but it could be IPv4 or IPv6
        if ip_addr.version == 4:
            mac_address = await hass.async_add_executor_job(
                partial(get_mac_address, ip=host)
            )
        else:
            ip_addr = IPv6Address(int(ip_addr))
            mac_address = await hass.async_add_executor_job(
                partial(get_mac_address, ip6=str(ip_addr))
            )
    if not mac_address:
        return None

    return format_mac(mac_address)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the Philips AirPurifier integration."""

    host = entry.data[CONF_HOST]
    model = entry.data[CONF_MODEL]
    name = entry.data[CONF_NAME]
    device_id = entry.data[CONF_DEVICE_ID]
    mac = await async_get_mac_address_from_host(hass, host)

    _LOGGER.debug("async_setup_entry called for host %s", host)

    try:
        client = await asyncio.wait_for(CoAPClient.create(host), timeout=25)
        _LOGGER.debug("got a valid client for host %s", host)

    except Exception as ex:
        _LOGGER.warning(r"Failed to connect to host %s: %s", host, ex)
        raise ConfigEntryNotReady from ex

    device_information = DeviceInformation(
        host=host, mac=mac, model=model, name=name, device_id=device_id
    )

    # check if we have status data, it will be missing in old entries
    if CONF_STATUS not in entry.data:
        _LOGGER.warning("No status data found for model %s, trying to fetch it", model)
        coordinator = Coordinator(hass, client, host, None)
        await coordinator.async_first_refresh()
        status = coordinator.status

        # update the entry with the status data
        new_data = {**entry.data}
        new_data[CONF_STATUS] = status
        hass.config_entries.async_update_entry(entry, data=new_data)

    else:
        status = entry.data[CONF_STATUS]
        coordinator = Coordinator(hass, client, host, status)

    # store the data in the hass.data
    config_entry_data = ConfigEntryData(
        device_information=device_information,
        coordinator=coordinator,
        latest_status=status,
        client=client,
    )
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = config_entry_data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register song playing services (only once)
    if not hass.services.has_service(DOMAIN, "play_song"):
        async def play_song_service(call):
            """Handle play song service calls."""
            song_name = call.data.get("song", "jingle_bells")
            
            # Play on all devices that support beep
            for entry_data in hass.data.get(DOMAIN, {}).values():
                await play_song_on_device(entry_data, song_name)

        async def play_song_on_device(config_entry_data: ConfigEntryData, song_name: str):
            """Play a song on a specific device using beep patterns."""
            
            # Check if device supports beep
            model_class = model_to_class.get(config_entry_data.device_information.model)
            if not model_class:
                return
                
            available_switches = []
            for cls in reversed(model_class.__mro__):
                cls_available_switches = getattr(cls, "AVAILABLE_SWITCHES", [])
                available_switches.extend(cls_available_switches)
                
            if PhilipsApi.NEW2_BEEP not in available_switches:
                _LOGGER.warning("Device %s does not support beep functionality", 
                              config_entry_data.device_information.name)
                return
                
            # Get song pattern
            from .const import SONG_PATTERNS
            pattern = SONG_PATTERNS.get(song_name)
            
            if not pattern:
                _LOGGER.error("Unknown song: %s", song_name)
                return
                
            _LOGGER.info("Playing song '%s' on device %s", song_name, 
                        config_entry_data.device_information.name)
            
            # Play the pattern
            try:
                for beep_duration, pause_duration in pattern:
                    # Turn beep on
                    await config_entry_data.client.set_control_value(PhilipsApi.NEW2_BEEP, 1)
                    await asyncio.sleep(beep_duration)
                    
                    # Turn beep off
                    await config_entry_data.client.set_control_value(PhilipsApi.NEW2_BEEP, 0)
                    await asyncio.sleep(pause_duration)
                    
            except Exception as e:
                _LOGGER.error("Error playing song %s: %s", song_name, e)

        # Register the service
        hass.services.async_register(
            DOMAIN,
            "play_song",
            play_song_service,
            schema=vol.Schema({
                vol.Optional("song", default="jingle_bells"): cv.string,
            })
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""

    for p in PLATFORMS:
        await hass.config_entries.async_forward_entry_unload(entry, p)

    config_entry_data: ConfigEntryData = hass.data[DOMAIN][entry.entry_id]
    await config_entry_data.coordinator.shutdown()

    hass.data[DOMAIN].pop(entry.entry_id)

    return True
