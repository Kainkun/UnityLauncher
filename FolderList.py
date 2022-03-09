import os
import sys
import typing
import MultiFileDialog

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog
from Generated.FolderListGenerated import Ui_FolderListWidget

class FolderList(QWidget):
    """
        A Widget that allows the user to select multiple Folders.

        Functions:
        - getContents() -> List[str]
        - setContents(List[str]) -> None
        - getUi() -> Ui_FolderListWidget

        Notes:
        - Makes heavy use of MultiFileDialog.py to present the File Selection Dialog.
    """

    def getContents(self) -> typing.List[str]:
        
        """ A list of folder paths that the user has selected, as strings. """

        folderList = self.getUi().FolderList
        result = []

        for index in range(folderList.count()):
            result.append(folderList.item(index).text())

        return result

    def setContents(self, contents: typing.List[str]) -> None:

        """ Updates the list of folder paths that the user has selected. """

        folderList = self.getUi().FolderList
        
        for item in contents:
            folderList.addItem(item)

    def getUi(self) -> Ui_FolderListWidget:

        """ Designer-generated user interface elements. """

        return self.__ui
    
    def __init__(self, 
            title: str = "Folder List",
            contents: typing.List[str] = {},
            parent: QWidget = None, 
            flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()
    ) -> None:
        """
            A Widget that allows the user to select multiple Folders.

            - Inputs:
                - parent - An optional QWidget that this object will be attached to on creation.
                - base - An optional QWidget that this object will inherit it's position from.
                - flags - Settings that can be used to customize what kind of QWidget this is: https://doc.qt.io/qt-5/qt.html#WindowType-enum

            - Outputs:
                - None

            - Notes:
                - Automatically converts relevent .ui files during construction to ensure it is up-to-date.
        """

        super().__init__(parent, flags)

        if not os.path.basename(sys.executable) == "UnityLauncher.exe":
            os.system("pyuic5 -x UI/FolderList.ui -o Generated/FolderListGenerated.py")

        self.__setupUI(parent, title)
        self.__setupEvents()

        self.setContents(contents)

    def __setupUI(self, parent: QWidget, title: str) -> None:
        
        """ Applies our pre-generated design to this procedural widget. """

        self.__ui = Ui_FolderListWidget()
        self.__ui.setupUi(parent)
        self.__ui.GroupProjectFolders.setTitle(title)

    def __setupEvents(self) -> None:

        """ Binds important logic to the UI elements that require them. """

        ui = self.getUi()

        ui.FolderList.itemSelectionChanged.connect(lambda: self.__handleSelectionChange())
        ui.ButtonRemoveFolder.clicked.connect(lambda: self.__removeFolder())
        ui.ButtonAddFolder.clicked.connect(lambda: self.__addFolder())

    def __handleSelectionChange(self):

        """ Disables or enabled the 'Remove' button if we are currently selecting anything. """

        ui = self.getUi()

        selectedItems = ui.FolderList.selectedItems()
        ui.ButtonRemoveFolder.setEnabled(len(selectedItems) > 0)

    def __addFolder(self):

        """ Prompts the user to select a folder from their directory, and adds it to the list. """

        ui = self.getUi()

        for path in MultiFileDialog.selectMultiple(QFileDialog.DirectoryOnly):
            ui.FolderList.addItem(path)

    def __removeFolder(self):

        """ Removes the folders that are currently selected from the list. """

        ui = self.getUi()

        folderList = ui.FolderList
        indexes = folderList.selectedIndexes()

        # Note: we traverse the list in reverse so we can remove elements mid-iteration without invalidating our index.
        indexes.reverse()

        for index in indexes:
            folderList.takeItem(index.row())

if __name__ == "__main__":

    # If you run this file on its own, show the folder list for debugging.

    application = QtWidgets.QApplication(sys.argv)

    folderList = FolderList()
    folderList.show()

    sys.exit(application.exec_())