[CmdletBinding()]
param (
    [Parameter()]
    [String]
    $Version
)
Set-Location $PSScriptRoot

Start-Process uv -ArgumentList "run pyinstaller --onefile --noconsole --distpath=dist/Windows/ --paths=src/Windows --name ClassificationBanner src/Windows/main.py" -wait

Get-ChildItem ".\ClassificationBanner_Install" | ForEach-Object {
    Copy-Item $_.FullName .\dist\Windows -Recurse
}
Get-ChildItem ".\src\Windows\Group Policy" | ForEach-Object {
    Copy-Item $_.FullName .\dist\Windows\SupportFiles -Recurse
}
Move-Item ".\dist\Windows\ClassificationBanner.exe" ".\dist\Windows\Files\ClassificationBanner.exe"

(Get-Content ".\dist\Windows\Invoke-AppDeployToolkit.ps1") -replace "AppVersion\s*=.*", "AppVersion                  = `'$($Version.Substring(1))`'" | Set-Content ".\dist\Windows\Invoke-AppDeployToolkit.ps1" -Force


Compress-Archive -Path .\dist\Windows\ -DestinationPath ".\dist\ClassificationBanner-$Version.zip"