pyinstaller --onefile --specpath .\build --workpath .\build\temp --distpath .\build\UnityLauncher --icon ..\Unity.ico .\UnityLauncher.pyw
robocopy "Config" "build\UnityLauncher\Config" /E
robocopy "Images" "build\UnityLauncher\Images" /E
pause