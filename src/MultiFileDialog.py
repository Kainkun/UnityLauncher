import sys
import typing

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView, QWidget


class MultiFileDialog(QFileDialog):
    """ 
        Prompts the user to select multiple files from their system.

        - Notes:
            - Code referenced from this forum post: 
            - https://stackoverflow.com/questions/38252419/how-to-get-qfiledialog-to-select-and-return-multiple-folders
    """

    def __init__(self,
                 fileMode: QFileDialog.FileMode = QFileDialog.AnyFile,
                 parent: typing.Optional[QWidget] = None,
                 flags: typing.Union[Qt.WindowFlags,
                                     Qt.WindowType] = Qt.WindowFlags()
                 ) -> None:
        """ Prompts the user to select multiple files from their system. """

        super().__init__(parent, flags)

        self.setFileMode(fileMode)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.__setSelectionMode(QListView, 'listView')
        self.__setSelectionMode(QTreeView)

    def __setSelectionMode(self, type: type, name: str = None) -> None:
        """ Assigns the ExtendedSelection mode to a target child of a dialog. """

        target = self.findChild(type, name)

        if target != None:
            target.setSelectionMode(QAbstractItemView.ExtendedSelection)


if __name__ == "__main__":

    # If you run this file on its own, show the folder list for debugging.

    application = QtWidgets.QApplication(sys.argv)

    fileDialog = MultiFileDialog(QFileDialog.DirectoryOnly)
    fileDialog.show()

    sys.exit(application.exec_())
