call Generate.bat
pyinstaller --onefile --noconsole --specpath .\build --workpath .\build\temp --distpath .\build\UnityLauncher --icon ..\images\Unity.ico .\UnityLauncher.py
pause