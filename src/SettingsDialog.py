import os
import sys
import typing

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog

from generated.SettingsGenerated import Ui_SettingsDialog
from src.Config import Config
from src.FolderListWidget import FolderListWidget

class SettingsDialog(QDialog):
    """
        Allows the user to change various configuration options relevent to the UnityLauncher.

        - Instance Variables:
            - projectFolderList: FolderList
            - editorFolderList: FolderList
            - config: Config
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

        self.config = Config()

        self.__setupUI()
        self.__setupEvents()

    def __setupUI(self) -> None:

        """ Constructs this widget from a pre-generated designer file, and populate it with relevent data from the config.json. """

        ui = Ui_SettingsDialog()
        ui.setupUi(self)

        config = self.config

        self.projectFolderList = FolderListWidget("Project Search Folders", config.getProjectFolders(), ui.ProjectFolderList)
        self.editorFolderList = FolderListWidget("Editor Search Folders", config.getEditorFolders(), ui.EditorFolderList)

    def __setupEvents(self) -> None:

        """ Assign logic to each of the interactable elements in the Settings page. """

        projectFolderUi = self.projectFolderList.getUi()
        editorFolderUi = self.editorFolderList.getUi()

        updateConfig = lambda: self.__updateConfig()

        editorFolderUi.ButtonAddFolder.clicked.connect(updateConfig)
        projectFolderUi.ButtonAddFolder.clicked.connect(updateConfig)
        editorFolderUi.ButtonRemoveFolder.clicked.connect(updateConfig)
        projectFolderUi.ButtonRemoveFolder.clicked.connect(updateConfig)

    def __updateConfig(self) -> None:

        """ Applys all relevent changes from the settings menu to the config. """

        config = self.config

        config.setProjectFolders(self.projectFolderList.getContents())
        config.setEditorFolders(self.editorFolderList.getContents())
        config.writeChanges()
        
if __name__ == "__main__":

    # If you run this file on its own, show the settings for debugging.

    application = QtWidgets.QApplication(sys.argv)

    settingsDialog = SettingsDialog()
    settingsDialog.show()

    sys.exit(application.exec_())