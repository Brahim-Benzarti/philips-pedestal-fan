#!/usr/bin/env python3
"""Test FanAttributes StrEnum for duplicate values."""

from enum import StrEnum

# Extract just the FanAttributes enum definition
class FanAttributes(StrEnum):
    """Fan attributes."""
    
    LABEL = "label"
    VALUE = "value"
    ICON = "icon"
    UNIT = "unit"
    DEVICE_CLASS = "device_class"
    STATE_CLASS = "state_class"
    ENTITY_CATEGORY = "entity_category"
    ENABLED = "enabled"

    # Device information
    NAME = "name"
    TYPE = "type"
    MODEL_ID = "modelid" 
    PRODUCT_ID = "ProductId"
    DEVICE_ID = "DeviceId"
    DEVICE_VERSION = "DeviceVersion"
    SOFTWARE_VERSION = "SoftwareVersion"
    HARDWARE_VERSION = "HardwareVersion"
    TOTAL = "total"
    TIME_REMAINING = "time_remaining"
    BEEP = "beep"
    AUTO_PLUS = "auto_plus"

    # Runtime information
    RUNTIME = "runtime"
    WI_FI_VERSION = "WifiVersion"
    ERROR_CODE = "err"
    ERROR = "error"
    MCU_VERSION = "MCUVersion"

    # Functions
    POWER = "pwr"
    OSCILLATION = "ose"
    NEW_OSCILLATION = "oscil"
    NEW2_OSCILLATION = "D7F80"
    CHILD_LOCK = "cl"
    
    # Fan speed
    FAN_SPEED = "om"
    NEW_FAN_SPEED = "fanspeed"
    NEW2_FAN_SPEED = "D80I0"
    
    # Modes
    MODE = "mode"
    NEW2_MODE = "D8260"
    SLEEP_MODE = "sleep" 
    AUTO_MODE = "auto"
    AUTO_QUICKDRY_MODE = "auto_quickdry"
    BACTERIA_VIRUS_MODE = "bacteria_virus"
    ALLERGEN = "allergen"
    GAS = "gas"
    PURIFICATION_ONLY_MODE = "purification_only"
    TWO_IN_ONE_MODE = "two_in_one"
    HEATING = "heating"
    CIRCULATION = "circulation"

    # Timer
    TIMER = "dt"
    TIMER_LEVEL = "dtrs"

    # Lighting
    LIGHT_BRIGHTNESS = "uil"
    NEW_LIGHT_BRIGHTNESS = "uilight"
    NEW2_LIGHT_BRIGHTNESS = "D86Z0"
    DISPLAY_BACKLIGHT = "backlight"

    # Temperature and humidity
    TEMPERATURE = "temp"
    HUMIDITY = "rh"
    TARGET_HUMIDITY = "rhset"
    NEW_TARGET_HUMIDITY = "targethumidity"
    NEW2_TARGET_HUMIDITY = "D82K0"
    WATER_LEVEL = "wl"

    # Air quality
    PM25 = "pm25"
    INDOOR_ALLERGEN_INDEX = "indoor_allergen_index"
    GAS_INDEX = "gas_index"
    INDOOR_TEMPERATURE = "indoor_temperature"

    # Filter information
    FILTER_ACTIVE_CARBON = "carbon_filter"
    FILTER_HEPA = "hepa_filter"
    FILTER_PRE = "pre_filter"
    FILTER_NANOPROTECT_CLEAN = "nanoprotect_prefilter_clean"
    FILTER_WICK = "wick_filter"

try:
    # Test that the enum can be created
    print("✓ FanAttributes StrEnum created successfully")
    
    # Check for duplicates
    values = []
    duplicates = []
    
    for attr_name in dir(FanAttributes):
        if not attr_name.startswith('_'):
            value = getattr(FanAttributes, attr_name)
            if value in values:
                duplicates.append((attr_name, value))
            else:
                values.append(value)
    
    if duplicates:
        print("✗ Duplicate values found:")
        for attr_name, value in duplicates:
            print(f"  {attr_name} = '{value}'")
    else:
        print("✓ No duplicate values found")
    
    # Check required attributes
    required = ['TOTAL', 'TIME_REMAINING', 'BEEP', 'AUTO_PLUS']
    for attr in required:
        if hasattr(FanAttributes, attr):
            print(f"✓ {attr} = '{getattr(FanAttributes, attr)}'")
        else:
            print(f"✗ Missing {attr}")
    
    print(f"✓ Total attributes: {len([attr for attr in dir(FanAttributes) if not attr.startswith('_')])}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
