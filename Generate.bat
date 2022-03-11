mkdir generated
pyuic5 -x ui/UnityLauncher.ui -o generated/UnityLauncherGenerated.py
pyuic5 -x ui/FolderList.ui -o generated/FolderListGenerated.py
pyuic5 -x ui/Settings.ui -o generated/SettingsGenerated.py
pyrcc5 resources.qrc -o resources_rc.py