"""Philips Air Purifier & Humidifier Buttons."""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ENTITY_CATEGORY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity, EntityCategory

from .config_entry_data import ConfigEntryData
from .const import DOMAIN, PhilipsApi
from .philips import PhilipsEntity, model_to_class

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[list[Entity], bool], None],
) -> None:
    """Set up the button platform."""

    config_entry_data: ConfigEntryData = hass.data[DOMAIN][entry.entry_id]

    model = config_entry_data.device_information.model

    model_class = model_to_class.get(model)
    if model_class:
        available_switches = []
        for cls in reversed(model_class.__mro__):
            cls_available_switches = getattr(cls, "AVAILABLE_SWITCHES", [])
            available_switches.extend(cls_available_switches)

        buttons = []
        
        # Add song buttons for devices that support beep
        if PhilipsApi.NEW2_BEEP in available_switches:
            buttons.append(JingleBellsButton(hass, entry, config_entry_data))

        async_add_entities(buttons, update_before_add=False)

    else:
        _LOGGER.error("Unsupported model: %s", model)
        return


class JingleBellsButton(PhilipsEntity, ButtonEntity):
    """Define a Jingle Bells song button."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: ConfigEntry,
        config_entry_data: ConfigEntryData,
    ) -> None:
        """Initialize the button."""

        super().__init__(hass, config, config_entry_data)

        self._model = config_entry_data.device_information.model
        self._attr_translation_key = "jingle_bells"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_icon = "mdi:music-note"

        model = config_entry_data.device_information.model
        device_id = config_entry_data.device_information.device_id
        self._attr_unique_id = f"{model}-{device_id}-jingle_bells_button"

    async def async_press(self) -> None:
        """Handle the button press."""
        # Call the play_song service for this specific device
        await self.hass.services.async_call(
            DOMAIN,
            "play_song",
            {
                "song": "jingle_bells"
            }
        )
        
        _LOGGER.info("Jingle Bells button pressed on device %s", 
                    self.config_entry_data.device_information.name)
