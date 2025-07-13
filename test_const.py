#!/usr/bin/env python3
"""Test script to check if FanAttributes loads without duplicate value errors."""

import sys
import importlib.util

# Load the const module directly to avoid other dependencies
spec = importlib.util.spec_from_file_location(
    "const", 
    "custom_components/philips_pedestal_fan/const.py"
)
const = importlib.util.module_from_spec(spec)

try:
    spec.loader.exec_module(const)
    print("✓ const.py loaded successfully")
    
    # Check if FanAttributes exists and has required attributes
    if hasattr(const, 'FanAttributes'):
        print("✓ FanAttributes class found")
        
        required_attrs = ['TOTAL', 'TIME_REMAINING', 'BEEP', 'AUTO_PLUS']
        for attr in required_attrs:
            if hasattr(const.FanAttributes, attr):
                print(f"✓ {attr} attribute found")
            else:
                print(f"✗ {attr} attribute missing")
        
        # Check for duplicate values
        values = []
        duplicates_found = False
        for attr_name in dir(const.FanAttributes):
            if not attr_name.startswith('_'):
                try:
                    value = getattr(const.FanAttributes, attr_name)
                    if value in values:
                        print(f"✗ Duplicate value found: {attr_name} = {value}")
                        duplicates_found = True
                    else:
                        values.append(value)
                except:
                    pass
        
        if not duplicates_found:
            print("✓ No duplicate values found in FanAttributes")
        
        print(f"✓ Total FanAttributes: {len([attr for attr in dir(const.FanAttributes) if not attr.startswith('_')])}")
    else:
        print("✗ FanAttributes class not found")

except Exception as e:
    print(f"✗ Error loading const.py: {e}")
    import traceback
    traceback.print_exc()
