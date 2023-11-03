## Unity Launcher
This PyQt Tool lists your Unity projects with icons and descriptions!
### Features
- Automatically populates Unity projects from chosen folders
- Set icons and descriptions to organize your projects
- Easily take in-engine screenshots that get set as project icons
- Sort and Search for projects

This tool is currently only for launching projects. To create new projects and install editors, please use Unity Hub :)

![Main Window Example](https://raw.githubusercontent.com/Kainkun/UnityLauncher/main/images/Examples/MainWindow.png)

## Instructions
1. To install it, download the .zip from the Releases tab and extract the file to wherever you'd like
2. UnityLauncher.exe runs the tool. I recommend right-clicking it and "Send To Desktop" to create a shortcut
    - You can also copy that shortcut to `%AppData%\Microsoft\Windows\Start Menu\Programs`
3. To start using Unity Launcher, click "Settings" on the top left and add your projects folder and your Unity editors folder

    ![Settings Popup Example](https://raw.githubusercontent.com/Kainkun/UnityLauncher/main/images/Examples/Settings.png)
4. Unity Launcher will auto-populate. Click a project to launch it!
5. You can right-click on a project to set its icon and description
6. The "Add Editor Scripts" button will copy a couple of handy editor scripts to your project
    - "Screenshot Project Icon" will take a screenshot of your game view and set that as your project icon
    - "Set Project Description" Will let you edit your project's description

    ![Unity Menu Bar Example](https://raw.githubusercontent.com/Kainkun/UnityLauncher/main/images/Examples/UnityMenuBar.png)

## Development
To build the executable files from the source, run **BuildOneDir.bat**.
These scripts will compile the project to a folder named "build".

If you make any changes to the UI via Qt Designer, make sure to run the **Generate.ps1** script!
This ensures that corresponding "generated/*.py" files are kept up to date, which the code uses.

##

<a href='https://ko-fi.com/kainkun' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' />
