call Generate.bat
pyinstaller --onedir --noconsole --specpath .\build --workpath .\build\temp --distpath .\build --paths .\generated --add-data ..\unityFiles\UnityLauncher\MenuItems.cs;.\unityFiles\UnityLauncher --add-data ..\unityFiles\UnityLauncher\TextureScale.cs;.\unityFiles\UnityLauncher --icon ..\images\Unity.ico .\UnityLauncher.py
pause