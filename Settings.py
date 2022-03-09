import os
import sys
import json
import typing

from Config import Config
from FolderList import FolderList
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog
from Generated.SettingsGenerated import Ui_SettingsDialog

# TODO: clean up code

class Settings(QDialog):
    """
        Allows the user to change various configuration options relevent to the UnityLauncher.

        - Instance Variables:
            - projectFolderUi: FolderList
            - editorFolderUi: FolderList
            - config: Config

        - Notes:
            - Interfaces with the config.json file to serialize and de-serialize the selected folders, so that the system remembers your selections.
    """

    def __init__(self, 
            parent: typing.Optional[QWidget] = None,
            flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()
    ) -> None:
        """
            Allows the user to change various configuration options relevent to the UnityLauncher.

            - Inputs: 
                - parent - An optional QWidget that this object will be attached to on creation.
                - flags - Settings that can be used to customize what kind of QWidget this is: https://doc.qt.io/qt-5/qt.html#WindowType-enum

            - Notes:
                - Automatically converts relevent .ui files during construction to ensure it is up-to-date.
        """

        super().__init__(parent, flags)

        if not os.path.basename(sys.executable) == "UnityLauncher.exe":
            os.system("pyuic5 -x UI/Settings.ui -o Generated/SettingsGenerated.py")

        self.config = Config()

        self.__setupUI()
        self.__setupEvents()

    def __setupUI(self) -> None:

        """ Constructs this widget from a pre-generated designer file, and populate it with relevent data from the config.json. """

        ui = Ui_SettingsDialog()
        ui.setupUi(self)

        self.projectFolderUi = self.__setupSearchFolder(title = "Project Search Folders", baseWidget = ui.ProjectFolderList)
        self.editorFolderUi = self.__setupSearchFolder(title = "Editor Search Folders", baseWidget = ui.EditorFolderList)

        self.projectFolderUi.setContents(self.config.getProjectFolders())
        self.editorFolderUi.setContents(self.config.getEditorFolders())

    def __setupSearchFolder(self, baseWidget: QWidget, title: str = "Search Folder") -> FolderList:

        folderWidget = FolderList(base = baseWidget)
        folderWidget.getUi().GroupProjectFolders.setTitle(title)
        return folderWidget

    def __setupEvents(self) -> None:
        projectFolderUi = self.projectFolderUi.getUi()
        editorFolderUi = self.editorFolderUi.getUi()

        updateConfig = lambda: self.__updateConfig()

        editorFolderUi.ButtonAddFolder.clicked.connect(updateConfig)
        projectFolderUi.ButtonAddFolder.clicked.connect(updateConfig)
        editorFolderUi.ButtonRemoveFolder.clicked.connect(updateConfig)
        projectFolderUi.ButtonRemoveFolder.clicked.connect(updateConfig)

    def __updateConfig(self) -> None:

        config = self.config

        config.setProjectFolders(self.projectFolderUi.getContents())
        config.setEditorFolders(self.editorFolderUi.getContents())
        config.writeChanges()
        
if __name__ == "__main__":

    # If you run this file on its own, show the settings for debugging.

    application = QtWidgets.QApplication(sys.argv)

    settingsDialog = Settings()
    settingsDialog.show()

    sys.exit(application.exec_())