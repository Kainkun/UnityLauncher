call Generate.bat
pyinstaller --onefile --noconsole --specpath .\build --workpath .\build\temp --distpath .\build\UnityLauncher --paths .\generated --add-data ..\unityFiles\UnityLauncher\MenuItems.cs;.\unityFiles\UnityLauncher --add-data ..\unityFiles\UnityLauncher\TextureScale.cs;.\unityFiles\UnityLauncher --icon ..\images\Unity.ico .\UnityLauncher.py
pause