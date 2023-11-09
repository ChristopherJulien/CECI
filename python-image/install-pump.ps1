# Get the current directory where the script is located
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the path to the ZIP file
$zipFilePath = Join-Path -Path $scriptDirectory -ChildPath "Pump33DriverSetup.zip"

# Define the path to the extraction folder
$extractionFolder = Join-Path -Path $scriptDirectory -ChildPath "DriverSetup"

# Check if the ZIP file exists
if (Test-Path $zipFilePath) {
    # Create the extraction folder if it doesn't exist
    if (!(Test-Path $extractionFolder)) {
        New-Item -ItemType Directory -Path $extractionFolder
    }

    # Extract the contents of the ZIP file
    Expand-Archive -Path $zipFilePath -DestinationPath $extractionFolder

    # Define the path to the subfolder where Driver Setup.exe is located
    $setupFolder = Join-Path -Path $extractionFolder -ChildPath "Pump 33 driver setup"

    # Define the path to Driver Setup.exe
    $setupExePath = Join-Path -Path $setupFolder -ChildPath "Driver Setup.exe"

    # Check if Driver Setup.exe exists in the subfolder
    if (Test-Path $setupExePath) {
        # Run Driver Setup.exe
        Start-Process -FilePath $setupExePath -Wait
        Write-Host "Driver Setup.exe executed successfully."
    } else {
        Write-Host "Driver Setup.exe not found in the subfolder."
    }
} else {
    Write-Host "ZIP file not found in the script's directory."
}
