# Philips Pedestal Fan Angle Control Examples

## Example Automations for Angle Control

### 1. Morning Routine - Center the Fan
```yaml
automation:
  - alias: "Morning Fan Center"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: select.select_option
        target:
          entity_id: select.your_fan_name_angle_preset
        data:
          option: center
```

### 2. Work from Home - Face the Desk
```yaml
automation:
  - alias: "Work Mode Fan Direction"
    trigger:
      - platform: state
        entity_id: person.your_name
        to: "home"
    condition:
      - condition: time
        after: "09:00:00"
        before: "17:00:00"
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
    action:
      - service: select.select_option
        target:
          entity_id: select.your_fan_name_angle_preset
        data:
          option: left_quarter  # Adjust based on your desk location
```

### 3. Sleep Mode - Wide Gentle Oscillation
```yaml
automation:
  - alias: "Sleep Mode Fan Angle"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: select.select_option
        target:
          entity_id: select.your_fan_name_angle_preset
        data:
          option: wide_oscillation
      - service: fan.set_preset_mode
        target:
          entity_id: fan.your_fan_name
        data:
          preset_mode: sleep
```

### 4. Custom Angle Based on Temperature
```yaml
automation:
  - alias: "Temperature Based Fan Direction"
    trigger:
      - platform: numeric_state
        entity_id: sensor.living_room_temperature
        above: 25
    action:
      - service: number.set_value
        target:
          entity_id: number.your_fan_name_oscillation
        data:
          value: 45  # Custom angle in degrees
```

### 5. Voice Control Examples
Add these to your voice assistant (like Google Assistant or Alexa):

- "Hey Google, set the fan to center position"
- "Hey Google, set the fan to left quarter"
- "Hey Google, set the fan angle to 90 degrees"

### 6. Dashboard Card Example
```yaml
type: entities
title: Fan Angle Control
entities:
  - entity: select.your_fan_name_angle_preset
    name: Angle Preset
  - entity: number.your_fan_name_oscillation
    name: Custom Angle
  - entity: switch.your_fan_name_oscillation
    name: Oscillation On/Off
```

## Script Examples

### Quick Position Scripts
```yaml
script:
  fan_face_sofa:
    alias: "Fan Face Sofa"
    sequence:
      - service: select.select_option
        target:
          entity_id: select.your_fan_name_angle_preset
        data:
          option: right_half

  fan_face_kitchen:
    alias: "Fan Face Kitchen" 
    sequence:
      - service: number.set_value
        target:
          entity_id: number.your_fan_name_oscillation
        data:
          value: 315  # Custom angle for kitchen direction
```

## Tips for Use

1. **Find Your Perfect Angles**: Use the number entity to find exact angles that work best for your room
2. **Create Custom Presets**: Note down the angles that work and create scripts for quick access
3. **Combine with Modes**: Use angle control together with speed and mode presets for complete comfort
4. **Test First**: Try different angles manually before setting up automations
5. **Room Layout**: Consider your room layout - angles will be relative to the fan's "front" position

## Supported Models
This angle control feature works with:
- Philips AMF765
- Philips AMF870
- Selected CX series models (CX3120, CX5120, CX3550)

Check your fan model in the device information to confirm support.
