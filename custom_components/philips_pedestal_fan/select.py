"""Philips Air Purifier & Humidifier Selects."""

from __future__ import annotations

from collections.abc import Callable
import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_DEVICE_CLASS, CONF_ENTITY_CATEGORY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity, EntityCategory

from .config_entry_data import ConfigEntryData
from .const import DOMAIN, OPTIONS, SELECT_TYPES, FanAttributes, PhilipsApi
from .philips import PhilipsEntity, model_to_class

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[list[Entity], bool], None],
) -> None:
    """Set up the select platform."""

    config_entry_data: ConfigEntryData = hass.data[DOMAIN][entry.entry_id]

    model = config_entry_data.device_information.model

    model_class = model_to_class.get(model)
    if model_class:
        available_selects = []

        for cls in reversed(model_class.__mro__):
            cls_available_selects = getattr(cls, "AVAILABLE_SELECTS", [])
            available_selects.extend(cls_available_selects)

        selects = [
            PhilipsSelect(hass, entry, config_entry_data, select)
            for select in SELECT_TYPES
            if select in available_selects
        ]

        # Add angle preset select for models with angle control
        model_class = model_to_class.get(model)
        if model_class:
            available_numbers = []
            for cls in reversed(model_class.__mro__):
                cls_available_numbers = getattr(cls, "AVAILABLE_NUMBERS", [])
                available_numbers.extend(cls_available_numbers)
            
            if PhilipsApi.NEW2_OSCILLATION in available_numbers:
                selects.append(PhilipsAnglePresetSelect(hass, entry, config_entry_data))

        async_add_entities(selects, update_before_add=False)

    else:
        _LOGGER.error("Unsupported model: %s", model)
        return


class PhilipsSelect(PhilipsEntity, SelectEntity):
    """Define a Philips AirPurifier select."""

    _attr_is_on: bool | None = False

    def __init__(
        self,
        hass: HomeAssistant,
        config: ConfigEntry,
        config_entry_data: ConfigEntryData,
        select: str,
    ) -> None:
        """Initialize the select."""

        super().__init__(hass, config, config_entry_data)

        self._model = config_entry_data.device_information.model

        self._description = SELECT_TYPES[select]
        self._attr_device_class = self._description.get(ATTR_DEVICE_CLASS)
        label = FanAttributes.LABEL
        label = label.partition("#")[0]
        self._attr_translation_key = self._description.get(FanAttributes.LABEL)
        self._attr_entity_category = self._description.get(CONF_ENTITY_CATEGORY)

        self._options = self._description.get(OPTIONS)
        self._attr_options = list(self._options.values())

        model = config_entry_data.device_information.model
        device_id = config_entry_data.device_information.device_id
        self._attr_unique_id = f"{model}-{device_id}-{select.lower()}"

        self._attrs: dict[str, Any] = {}
        self.kind = select.partition("#")[0]

    @property
    def current_option(self) -> str:
        """Return the currently selected option."""
        option = self._device_status.get(self.kind)
        current_option = str(self._options.get(option))
        _LOGGER.debug(
            "option: %s, returning as current_option: %s", option, current_option
        )
        return current_option

    async def async_select_option(self, option: str) -> None:
        """Select an option."""
        if option is None or len(option) == 0:
            _LOGGER.error("Cannot set empty option '%s'", option)
            return
        try:
            option_key = next(
                key for key, value in self._options.items() if value == option
            )
            _LOGGER.debug(
                "async_selection_option, kind: %s - option: %s - value: %s",
                self.kind,
                option,
                option_key,
            )
            await self.coordinator.client.set_control_value(self.kind, option_key)
            self._device_status[self.kind] = option_key
            self._handle_coordinator_update()

        except KeyError as e:
            _LOGGER.error("Invalid option key: '%s' with error: %s", option, e)
        except ValueError as e:
            _LOGGER.error("Invalid value for option: '%s' with error: %s", option, e)


class PhilipsAnglePresetSelect(PhilipsEntity, SelectEntity):
    """Define a Philips fan angle preset selector."""

    def __init__(
        self,
        hass: HomeAssistant,
        config: ConfigEntry,
        config_entry_data: ConfigEntryData,
    ) -> None:
        """Initialize the angle preset select."""

        super().__init__(hass, config, config_entry_data)

        self._model = config_entry_data.device_information.model
        self._attr_translation_key = "angle_preset"
        self._attr_entity_category = EntityCategory.CONFIG

        # Define the angle preset options
        self._angle_presets = {
            "center": 0,
            "left_quarter": 90,
            "left_half": 135,
            "right_quarter": 270,
            "right_half": 225,
            "full_left": 180,
            "wide_oscillation": 180,
            "narrow_oscillation": 90,
        }
        
        self._attr_options = list(self._angle_presets.keys())

        model = config_entry_data.device_information.model
        device_id = config_entry_data.device_information.device_id
        self._attr_unique_id = f"{model}-{device_id}-angle_preset"

    @property
    def current_option(self) -> str | None:
        """Return the currently selected angle preset."""
        current_angle = self._device_status.get(PhilipsApi.NEW2_OSCILLATION)
        if current_angle is None:
            return None
            
        # Find the closest preset
        for preset, angle in self._angle_presets.items():
            if abs(current_angle - angle) <= 5:  # 5-degree tolerance
                return preset
        
        # If no preset matches, return None (custom angle)
        return None

    async def async_select_option(self, option: str) -> None:
        """Select an angle preset."""
        if option not in self._angle_presets:
            _LOGGER.error("Invalid angle preset: %s", option)
            return
            
        target_angle = self._angle_presets[option]
        
        try:
            await self.coordinator.client.set_control_value(
                PhilipsApi.NEW2_OSCILLATION, target_angle
            )
            self._device_status[PhilipsApi.NEW2_OSCILLATION] = target_angle
            self._handle_coordinator_update()
            
        except Exception as e:
            _LOGGER.error("Failed to set angle preset %s: %s", option, e)
