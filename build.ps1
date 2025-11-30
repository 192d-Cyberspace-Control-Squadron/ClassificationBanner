Start-Process uv -ArgumentList "run pyinstaller --onefile --noconsole --distpath=dist/Windows/ --paths=src/Windows --name ClassificationBanner src/Windows/main.py"

Get-ChildItem ".\ClassificationBanner_Install" | ForEach-Object {
    Copy-Item $_.FullName .\dist\Windows -Recurse
}
Copy-Item ".\src\Windows\Group Policy" .\dist\Windows\SupportFiles -Recurse
Move-Item ".\dist\Windows\ClassificationBanner.exe" ".\dist\Windows\Files\ClassificationBanner.exe"

Compress-Archive -Path .\dist\Windows\