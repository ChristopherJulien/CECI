# Get the current directory where the script is located
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the path to the installer file
$installerPath = Join-Path -Path $scriptDirectory -ChildPath "Logic-2.4.10-windows-x64.exe"

# Check if the installer file exists
if (Test-Path $installerPath) {
    # Run the installer
    Start-Process -FilePath $installerPath -Wait
    Write-Host "Installation completed successfully."
} else {
    Write-Host "Installer file not found in the script's directory."
}
