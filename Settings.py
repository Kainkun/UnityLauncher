import os
import sys
import json
import typing

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog

from Generated.SettingsGenerated import Ui_SettingsDialog
from Generated.FolderListGenerated import Ui_FolderListWidget
from FolderList import FolderList


class Settings(QDialog):

    def __init__(self, 
            parent: typing.Optional[QWidget] = None,
            flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()
    ) -> None:

        # Convert our UI design into python code.
        os.system("pyuic5 -x UI/FolderList.ui -o Generated/FolderListGenerated.py")
        os.system("pyuic5 -x UI/Settings.ui -o Generated/SettingsGenerated.py")

        super().__init__(parent, flags)
        self.__setupUI()
        self.__setupEvents()

    def __setupUI(self) -> None:

        ui = Ui_SettingsDialog()
        ui.setupUi(self)

        with open("config.json") as configFile:
            self.settingsData = json.load(configFile)

        self.projectFolderUi = self.__setupSearchFolder(title = "Project Search Folders", baseWidget = ui.ProjectFolderList)
        self.editorFolderUi = self.__setupSearchFolder(title = "Editor Search Folders", baseWidget = ui.EditorFolderList)

        self.projectFolderUi.setContents(self.settingsData["ProjectFolders"])
        self.editorFolderUi.setContents(self.settingsData["EditorFolders"])

    def __setupSearchFolder(self, 
            baseWidget: QWidget,
            title: str = "Search Folder"
    ) -> FolderList:

        folderWidget = FolderList(base = baseWidget)
        folderWidget.ui().GroupProjectFolders.setTitle(title)
        return folderWidget

    def __setupEvents(self) -> None:
        self.projectFolderUi.ui().ButtonAddFolder.clicked.connect(lambda: self.__updateConfig())
        self.projectFolderUi.ui().ButtonRemoveFolder.clicked.connect(lambda: self.__updateConfig())
        self.editorFolderUi.ui().ButtonAddFolder.clicked.connect(lambda: self.__updateConfig())
        self.editorFolderUi.ui().ButtonRemoveFolder.clicked.connect(lambda: self.__updateConfig())

    def __updateConfig(self) -> None:
        self.settingsData["ProjectFolders"] = self.projectFolderUi.getContents()
        self.settingsData["EditorFolders"] = self.editorFolderUi.getContents()

        with open("config.json", mode = "w+") as config:
            json.dump(self.settingsData, config, indent=4, sort_keys=True)
        
# If you run this file on its own, show the settings for debugging.
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)

    settingsDialog = Settings()
    settingsDialog.show()

    sys.exit(application.exec_())