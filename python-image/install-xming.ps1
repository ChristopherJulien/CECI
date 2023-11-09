# Get the current directory where the script is located
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the path to the installer file
$installerPath = Join-Path -Path $scriptDirectory -ChildPath "Xming-6-9-0-31-setup.exe"

# Check if the installer file exists
if (Test-Path $installerPath) {
    # Run the installer
    Start-Process -FilePath $installerPath -Wait
    Write-Host "Installation Xming completed successfully."
} else {
    Write-Host "Installer file not found in the script's directory."
}