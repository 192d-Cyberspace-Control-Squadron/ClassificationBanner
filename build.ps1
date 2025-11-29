Start-Process uv -ArgumentList "run pyinstaller --onefile --noconsole --distpath=dist/Windows/ --paths=src/Windows --name ClassificationBanner src/Windows/main.py"
Copy-Item ".\src\Windows\Group Policy" .\dist\Windows -Recurse
Compress-Archive -Path .\dist\Windows\ 