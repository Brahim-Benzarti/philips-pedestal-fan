# Changes Made to Fork the Repository

## Summary
I've successfully transformed the original Philips AirPurifier integration into your own Philips Pedestal Fan integration. Here are all the changes made:

## Files Modified

### 1. README.md
- Updated GitHub URLs to point to YOUR_GITHUB_USERNAME/philips-pedestal-fan
- Changed integration name from "Philips AirPurifier" to "Philips Pedestal Fan"
- Added clear attribution to the original work
- Updated description to focus on pedestal fans
- Updated configuration instructions
- Updated icon paths to use new directory structure

### 2. custom_components/philips_pedestal_fan/manifest.json
- Changed domain from "philips_airpurifier_coap" to "philips_pedestal_fan"
- Changed name to "Philips Pedestal Fan"
- Updated codeowners to YOUR_GITHUB_USERNAME
- Updated documentation and issue tracker URLs

### 3. custom_components/philips_pedestal_fan/const.py
- Changed DOMAIN constant to "philips_pedestal_fan"
- Changed DEFAULT_NAME to "Philips Pedestal Fan"

### 4. custom_components/philips_pedestal_fan/strings.json
- Updated title and display names to "Philips Pedestal Fan"

### 5. hacs.json
- Changed name to "Philips Pedestal Fan"

### 6. Directory Structure
- Renamed custom_components/philips_airpurifier_coap to custom_components/philips_pedestal_fan

### 7. JavaScript Files
- Updated custom_components/philips_pedestal_fan/main.js - changed DOMAIN constant
- Updated js/main.js - changed DOMAIN constant
- Updated js/main.min.js - changed DOMAIN constant

### 8. GitHub Workflow
- Updated .github/workflows/update-manifest.yml to use new paths and username

### 9. Shell Script
- Updated aioairctrl-shell.sh to use new manifest path

## New Files Created

### 10. SETUP_GUIDE.md
- Comprehensive setup instructions
- List of all changes made
- Next steps for customization

### 11. setup.ps1
- PowerShell script to automatically replace YOUR_GITHUB_USERNAME with actual username
- Handles all files that need username replacement

## Next Steps

1. **Replace Placeholder Username**: Run the setup.ps1 script with your actual GitHub username:
   ```powershell
   .\setup.ps1 -GitHubUsername "your-actual-username"
   ```

2. **Test the Integration**: Install and test with your pedestal fan to ensure it works

3. **Customize for Your Device**: 
   - Update device discovery MAC addresses in manifest.json if needed
   - Modify features specific to your pedestal fan model
   - Update supported device models

4. **Create GitHub Repository**:
   - Create a new repository named "philips-pedestal-fan"
   - Push your changes
   - Create releases for HACS distribution

5. **Submit to HACS** (optional): Once stable, consider submitting to HACS default repositories

## Legal Considerations
- Proper attribution maintained to original authors
- Original license terms preserved where applicable
- Clear identification as a fork/derivative work

All placeholder values (YOUR_GITHUB_USERNAME) need to be replaced with your actual information before use.
