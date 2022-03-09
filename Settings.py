import os
import sys
import typing

# Convert our UI design into python code.
os.system("pyuic5 -x UI/FolderList.ui -o Generated/FolderListGenerated.py")
os.system("pyuic5 -x UI/Settings.ui -o Generated/SettingsGenerated.py")

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog

# Import generated UI code.
from Generated.SettingsGenerated import Ui_SettingsDialog
from Generated.FolderListGenerated import Ui_FolderListWidget

class Settings(QDialog):

    def __init__(self, 
            parent: typing.Optional[QWidget] = None,
            flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()
    ) -> None:

        super().__init__(parent, flags)

        ui = Ui_SettingsDialog()
        self.__setupUI(ui)
        self.__setupEvents(ui)

    def __setupUI(self, ui: Ui_SettingsDialog) -> None:

        ui.setupUi(self)
        self.projectSearchWidget = self.__setupSearchFolder(title = "Project Search Folders", baseWidget = ui.ProjectFolderList)
        self.editorSearchWidget = self.__setupSearchFolder(title = "Editor Search Folders", baseWidget = ui.EditorFolderList)

    def __setupSearchFolder(self, 
            baseWidget: QWidget,
            title: str = "Search Folder"
    ) -> Ui_FolderListWidget:

        folderWidget = Ui_FolderListWidget()
        folderWidget.setupUi(baseWidget)
        folderWidget.GroupProjectFolders.setTitle(title)

        return folderWidget

    def __setupEvents(self, ui: Ui_SettingsDialog) -> None:
        self.projectSearchWidget.ButtonAddFolder.clicked.connect(lambda: print("Add project folder"))
        self.projectSearchWidget.ButtonRemoveFolder.clicked.connect(lambda: print("Remove project folder"))
        self.editorSearchWidget.ButtonAddFolder.clicked.connect(lambda: print("Add editor folder"))
        self.editorSearchWidget.ButtonRemoveFolder.clicked.connect(lambda: print("Remove editor folder"))


# If you run this file on its own, show the settings for debugging.
if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)

    settingsDialog = Settings()
    settingsDialog.show()

    sys.exit(application.exec_())