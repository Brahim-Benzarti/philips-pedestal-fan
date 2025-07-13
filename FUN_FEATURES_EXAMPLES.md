# 🎵 Fun Features Examples

## Song Button Usage

### Simple Button Press
1. Go to your fan device in Home Assistant
2. Look for the "🎵 Jingle Bells" button in the controls
3. Press it to play the song!

## Service Examples

### Play Song via Service Call
```yaml
# Basic service call
service: philips_pedestal_fan.play_song
data:
  song: jingle_bells
```

### Play on Specific Device
```yaml
service: philips_pedestal_fan.play_song
data:
  entity_id: fan.your_fan_name
  song: jingle_bells
```

## Automation Examples

### 1. Christmas Morning Surprise
```yaml
automation:
  - alias: "Christmas Morning Fan Song"
    trigger:
      - platform: time
        at: "08:00:00"
    condition:
      - condition: template
        value_template: "{{ now().month == 12 and now().day == 25 }}"
    action:
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
      - service: notify.family
        data:
          message: "🎄 Merry Christmas! Your fan is singing! 🎵"
```

### 2. Birthday Celebration
```yaml
automation:
  - alias: "Birthday Fan Celebration"
    trigger:
      - platform: state
        entity_id: person.birthday_person
        to: "home"
    condition:
      - condition: template
        value_template: >
          {{ now().strftime('%m-%d') == states('input_text.birthday_date') }}
    action:
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells  # Can be expanded with "happy_birthday" later
      - delay: "00:00:30"
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
```

### 3. Hourly Chime (Holiday Season)
```yaml
automation:
  - alias: "Holiday Hourly Chime"
    trigger:
      - platform: time_pattern
        minutes: 0
    condition:
      - condition: time
        after: "09:00:00"
        before: "21:00:00"
      - condition: template
        value_template: "{{ now().month == 12 }}"
    action:
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
```

### 4. Timer Completion Celebration
```yaml
automation:
  - alias: "Cooking Timer Fan Song"
    trigger:
      - platform: event
        event_type: timer.finished
        event_data:
          entity_id: timer.cooking_timer
    action:
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
      - service: notify.kitchen_display
        data:
          message: "🍳 Cooking timer finished! 🎵"
```

### 5. Welcome Home Song
```yaml
automation:
  - alias: "Welcome Home Fan Song"
    trigger:
      - platform: state
        entity_id: person.family_member
        from: "not_home"
        to: "home"
    condition:
      - condition: time
        after: "17:00:00"
        before: "22:00:00"
    action:
      - delay: "00:00:05"  # Give them time to get inside
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
```

## Script Examples

### Fan Concert Mode
```yaml
script:
  fan_concert:
    alias: "Fan Concert"
    sequence:
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
      - delay: "00:00:10"
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
      - service: notify.family
        data:
          message: "🎵 Fan concert complete! 🎭"
```

### Musical Fan Dance
```yaml
script:
  fan_dance:
    alias: "Musical Fan Dance"
    sequence:
      # Start the music
      - service: philips_pedestal_fan.play_song
        data:
          song: jingle_bells
      # Dance with angles
      - parallel:
          - sequence:
              - delay: "00:00:02"
              - service: select.select_option
                target:
                  entity_id: select.your_fan_angle_preset
                data:
                  option: left_quarter
              - delay: "00:00:02"
              - service: select.select_option
                target:
                  entity_id: select.your_fan_angle_preset
                data:
                  option: right_quarter
              - delay: "00:00:02"
              - service: select.select_option
                target:
                  entity_id: select.your_fan_angle_preset
                data:
                  option: center
```

## Dashboard Examples

### Fun Control Card
```yaml
type: entities
title: 🎵 Fan Fun Zone
entities:
  - entity: button.your_fan_jingle_bells
    name: Play Jingle Bells
  - entity: select.your_fan_angle_preset
    name: Dance Position
  - type: call-service
    name: Fan Concert
    service: script.fan_concert
    icon: mdi:music-note-multiple
```

### Holiday Theme Card
```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      ## 🎄 Holiday Fan Controls 🎄
  - type: entities
    entities:
      - entity: button.your_fan_jingle_bells
        name: 🎵 Play Christmas Song
      - entity: select.your_fan_angle_preset
        name: 🌟 Fan Position
  - type: horizontal-stack
    cards:
      - type: button
        tap_action:
          action: call-service
          service: philips_pedestal_fan.play_song
          service_data:
            song: jingle_bells
        name: Jingle Bells
        icon: mdi:music-note
```

## Voice Assistant Integration

### Google Assistant / Alexa Examples
Add these to your voice assistant routines:

**"Hey Google, play fan music"**
```yaml
service: philips_pedestal_fan.play_song
data:
  song: jingle_bells
```

**"Hey Google, fan concert mode"**
```yaml
service: script.fan_concert
```

## Tips for Maximum Fun

1. **Holiday Integration**: Use with holiday automations for festive surprises
2. **Timer Alerts**: Perfect for cooking timers, workout intervals, or reminders
3. **Guest Entertainment**: Surprise visitors with your musical fan
4. **Kids' Fun**: Great for entertaining children or marking special moments
5. **Celebration Mode**: Use for birthdays, achievements, or just because!

## Expandable Song Library

The system is designed to be easily expandable. Future songs could include:
- Happy Birthday
- Wedding March
- Star Wars Theme
- Mario Theme
- Custom melodies

## Supported Models

The fun song features work with any Philips fan model that supports beep functionality:
- AMF765 ✅
- AMF870 ✅
- Most modern CX and AC series models ✅

Check your device entities - if you see a "Beep" switch, you can use the song features!
