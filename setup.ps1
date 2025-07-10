# Setup script for Philips Pedestal Fan Integration
# Replace YOUR_GITHUB_USERNAME with your actual GitHub username

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername
)

Write-Host "Setting up Philips Pedestal Fan Integration with username: $GitHubUsername"

$files = @(
    "README.md",
    "custom_components\philips_pedestal_fan\manifest.json",
    ".github\workflows\update-manifest.yml"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Updating $file..."
        (Get-Content $file) -replace "YOUR_GITHUB_USERNAME", $GitHubUsername | Set-Content $file
        Write-Host "✓ Updated $file"
    } else {
        Write-Warning "File not found: $file"
    }
}

Write-Host "`nSetup complete! Your integration is now configured with username: $GitHubUsername"
Write-Host "Next steps:"
Write-Host "1. Test the integration with your pedestal fan"
Write-Host "2. Make any necessary code adjustments"
Write-Host "3. Create a new GitHub repository"
Write-Host "4. Push your changes to GitHub"
Write-Host "5. Consider submitting to HACS once stable"
