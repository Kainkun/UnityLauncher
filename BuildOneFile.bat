call Generate.bat
pyinstaller --onefile --noconsole --specpath .\build --workpath .\build\temp --distpath .\build\UnityLauncher --paths .\generated --icon ..\images\Unity.ico .\UnityLauncher.py
pause