New-Item -ItemType Directory -Force -Path generated
pyuic5 -x designer/UnityLauncher.ui -o generated/UnityLauncherGenerated.py
pyuic5 -x designer/FolderList.ui -o generated/FolderListGenerated.py
pyuic5 -x designer/Settings.ui -o generated/SettingsGenerated.py
pyrcc5 designer/resources.qrc -o generated/resources_rc.py
((Get-Content -path generated/UnityLauncherGenerated.py -Raw) -replace 'import resources_rc','import generated.resources_rc') | Set-Content -Path generated/UnityLauncherGenerated.py