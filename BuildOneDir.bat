call Generate.bat
pyinstaller --onedir --specpath .\build --workpath .\build\temp --distpath .\build --paths .\generated --icon ..\images\Unity.ico .\UnityLauncher.py
pause