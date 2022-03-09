import os
import sys
import typing
from FolderList import FolderList

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog

from Generated.SettingsGenerated import Ui_SettingsDialog
from Generated.FolderListGenerated import Ui_FolderListWidget

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

    def __setupUI(self) -> None:

        ui = Ui_SettingsDialog()
        ui.setupUi(self)
        
        self.__setupSearchFolder(title = "Project Search Folders", baseWidget = ui.ProjectFolderList)
        self.__setupSearchFolder(title = "Editor Search Folders", baseWidget = ui.EditorFolderList)

    def __setupSearchFolder(self, 
            baseWidget: QWidget,
            title: str = "Search Folder"
    ) -> Ui_FolderListWidget:

        folderWidget = FolderList(base = baseWidget)
        folderWidget.ui().GroupProjectFolders.setTitle(title)
        return folderWidget

# If you run this file on its own, show the settings for debugging.
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)

    settingsDialog = Settings()
    settingsDialog.show()

    sys.exit(application.exec_())