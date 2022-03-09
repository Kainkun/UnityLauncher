import os
import sys
import typing
import MultiFileDialog

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QFileDialog, QListView, QAbstractItemView, QTreeView
from Generated.FolderListGenerated import Ui_FolderListWidget

# TODO: clean up code

class FolderList(QWidget):
    def getContents(self) -> typing.List[str]:
        folderList = self.ui().FolderList
        result: typing.List[str] = []

        for index in range(folderList.count()):
            result.append(folderList.item(index).text())

        return result

    def setContents(self, contents: typing.List[str]) -> None:
        folderList = self.ui().FolderList
        
        for item in contents:
            folderList.addItem(item)

    def ui(self) -> Ui_FolderListWidget:
        return self.__ui
    
    def __init__(self, 
            parent: typing.Optional['QWidget'] = None, 
            base: typing.Optional['QWidget'] = None,
            flags: typing.Union[QtCore.Qt.WindowFlags, QtCore.Qt.WindowType] = QtCore.Qt.WindowFlags()
    ) -> None:

        # Convert our UI design into python code.
        os.system("pyuic5 -x UI/FolderList.ui -o Generated/FolderListGenerated.py")

        super().__init__(parent, flags)
        self.__setupUI(base)
        self.__setupEvents()

    def __setupUI(self, base: QWidget) -> None:
        self.__ui = Ui_FolderListWidget()
        self.__ui.setupUi(base if base != None else self)

    def __setupEvents(self) -> None:
        ui = self.ui()
        ui.FolderList.itemSelectionChanged.connect(lambda: self.__handleSelectionChange(ui))
        ui.ButtonRemoveFolder.clicked.connect(lambda: self.__removeFolder(ui))
        ui.ButtonAddFolder.clicked.connect(lambda: self.__addFolder(ui))

    def __handleSelectionChange(self, ui: Ui_FolderListWidget):
        selectedItems = ui.FolderList.selectedItems()
        ui.ButtonRemoveFolder.setEnabled(len(selectedItems) > 0)

    def __addFolder(self, ui: Ui_FolderListWidget):
        paths = MultiFileDialog.selectMultiple(QFileDialog.DirectoryOnly)

        for path in paths:
            ui.FolderList.addItem(path)

    def __removeFolder(self, ui: Ui_FolderListWidget):
        folderList = ui.FolderList
        indexes = folderList.selectedIndexes()
        indexes.reverse()

        for index in indexes:
            folderList.takeItem(index.row())

if __name__ == "__main__":

    # If you run this file on its own, show the folder list for debugging.

    application = QtWidgets.QApplication(sys.argv)

    folderList = FolderList()
    folderList.show()

    sys.exit(application.exec_())