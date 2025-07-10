<div align="center">

# 🌀 Philips Pedestal Fan Integration

[![HACS Default][hacs_shield]][hacs]
[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub Stars][stars_shield]][stars]
[![License][license_shield]][license]

**Transform your Philips pedestal fan into a smart Home Assistant device** ✨

*Local control • Real-time monitoring • No cloud dependency*

---

</div>

## 🚀 Features

- 🏠 **Local Control** - Direct communication with your fan via CoAP
- 📊 **Real-time Monitoring** - Air quality, temperature, and humidity sensors
- 🌪️ **Smart Automation** - Fan speed, oscillation, and purifier modes
- 🎛️ **Full Integration** - Native Home Assistant controls and automations
- 🔒 **Privacy First** - No data sent to cloud services
- 🎨 **Custom Icons** - Beautiful vector icons for all controls

## 📋 Supported Devices

This integration is specifically designed for **Philips pedestal fans with air purifier functionality**. It's based on the excellent reverse engineering work of the community.

> **⚠️ Stability Notice**: Due to firmware limitations in Philips devices, connection stability may vary. Occasional restarts of the device or Home Assistant may be needed.

## 🛠️ Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the menu (⋮) and select "Custom repositories"
4. Add `https://github.com/Brahim-Benzarti/philips-pedestal-fan` as an Integration
5. Search for "Philips Pedestal Fan" and install

### Manual Installation

1. Download the latest release
2. Copy `custom_components/philips_pedestal_fan` to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## ⚙️ Configuration

### Auto-Discovery
The integration automatically discovers compatible devices on your network.

### Manual Setup
1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for **Philips Pedestal Fan**
4. Enter your device's IP address or hostname

## 🎯 What You Get

- **Fan Control** - Speed, oscillation, sleep mode
- **Air Purifier** - Filter monitoring, air quality sensors
- **Environmental Sensors** - Temperature, humidity, PM2.5, allergens
- **Smart Features** - Child lock, timers, light controls
- **Status Monitoring** - Filter life, connectivity, error states

## 🏆 Credits & Acknowledgments

This integration stands on the shoulders of giants. Huge thanks to:

- 🔬 **@rgerganov** - Original reverse engineering pioneer ([py-air-control](https://github.com/rgerganov/py-air-control))
- 🏗️ **@betaboon** - Initial CoAP integration foundation
- 🔧 **@Denaun** - Major rework and improvements
- 🚀 **@kongo09** - Enhanced integration and maintenance ([original repo](https://github.com/kongo09/philips-airpurifier-coap))
- 🤝 **Community Contributors** - @mhetzi, @Kraineff, @shexbeer and many others

*Adapted for pedestal fans by* **@Brahim-Benzarti**

## ☕ Support This Project

If this pedestal fan integration helps you, consider supporting the development:

<div align="center">

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://buymeacoffee.com/brahimbenzarti)

</div>

## 📄 License

This project maintains the original licensing terms and attributions.

---

<div align="center">

**Made with ❤️ for the Home Assistant community**

[Report Bug](https://github.com/Brahim-Benzarti/philips-pedestal-fan/issues) • [Request Feature](https://github.com/Brahim-Benzarti/philips-pedestal-fan/issues) • [Discussions](https://github.com/Brahim-Benzarti/philips-pedestal-fan/discussions)

</div>

[hacs_shield]: https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge
[hacs]: https://hacs.xyz/docs/default_repositories
[latest_release]: https://github.com/Brahim-Benzarti/philips-pedestal-fan/releases/latest
[releases_shield]: https://img.shields.io/github/release/Brahim-Benzarti/philips-pedestal-fan.svg?style=for-the-badge
[stars_shield]: https://img.shields.io/github/stars/Brahim-Benzarti/philips-pedestal-fan.svg?style=for-the-badge
[stars]: https://github.com/Brahim-Benzarti/philips-pedestal-fan/stargazers
[license_shield]: https://img.shields.io/github/license/Brahim-Benzarti/philips-pedestal-fan.svg?style=for-the-badge
[license]: https://github.com/Brahim-Benzarti/philips-pedestal-fan/blob/main/LICENSE

