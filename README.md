[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Usage:
```yaml
fan:
  platform: philips_airpurifier
  host: 192.168.0.17
  model: ac4236
```

## Configuration variables:
Field | Value | Necessity | Description
--- | --- | --- | ---
platform | `philips_airpurifier` | *Required* | The platform name.
host | 192.168.0.17 | *Required* | IP address of the Purifier.
model | ac4236 | *Required* | Model of the Purifier.
name | Philips Air Purifier | Optional | Name of the Fan.
***
