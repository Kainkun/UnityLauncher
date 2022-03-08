pyinstaller --onefile --noconsole --specpath .\build --workpath .\build\temp --distpath .\build\UnityLauncher --icon ..\Unity.ico .\UnityLauncher.py
robocopy "Config" "build\UnityLauncher\Config" /E
robocopy "Images" "build\UnityLauncher\Images" /E
pause