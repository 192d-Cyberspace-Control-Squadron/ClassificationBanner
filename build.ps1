[CmdletBinding()]
param (
    [Parameter()]
    [String]
    $Version
)
Set-Location $PSScriptRoot

Start-Process uv -ArgumentList "run pyinstaller --onefile --noconsole --distpath=$PSScriptRoot\dist\Windows\ --paths=$PSScriptRoot\src\Windows --name ClassificationBanner $PSScriptRoot/src/Windows/main.py" -wait

Get-ChildItem "$PSScriptRoot\ClassificationBanner_Install" | ForEach-Object {
    Copy-Item $_.FullName .\dist\Windows -Recurse
}
Get-ChildItem "$PSScriptRoot\src\Windows\Group Policy" | ForEach-Object {
    Copy-Item $_.FullName .\dist\Windows\SupportFiles -Recurse
}
Move-Item "$PSScriptRoot\dist\Windows\ClassificationBanner.exe" "$PSScriptRoot\dist\Windows\Files\ClassificationBanner.exe"

(Get-Content "$PSScriptRoot\dist\Windows\Invoke-AppDeployToolkit.ps1") -replace "AppVersion\s*=.*", "AppVersion                  = `'$($Version.Substring(1))`'" | Set-Content ".\dist\Windows\Invoke-AppDeployToolkit.ps1" -Force


Compress-Archive -Path "$PSScriptRoot\dist\Windows\" -DestinationPath "$PSScriptRoot\dist\ClassificationBanner-$Version.zip"