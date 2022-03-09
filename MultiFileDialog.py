import typing

from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView

def selectMultiple(fileMode: QFileDialog.FileMode = QFileDialog.AnyFile) -> typing.List[str]:
    """ 
        Prompts the user to select multiple files from their system.

        - Inputs:
            - fileMode - the types of files that should be selectable by the user. Defaults to QFileDialog.AnyFile.
        
        - Outputs:
            - A list of paths to the selected files.

        Code referenced from this forum post:
        https://stackoverflow.com/questions/38252419/how-to-get-qfiledialog-to-select-and-return-multiple-folders
    """
    
    file_dialog = QFileDialog()
    file_dialog.setFileMode(fileMode)
    file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)

    __setSelectionMode(file_dialog, QListView, 'listView')
    __setSelectionMode(file_dialog, QTreeView)

    result: typing.List[str] = []

    if file_dialog.exec():
        result = file_dialog.selectedFiles()

    return result

def __setSelectionMode(dialog: QFileDialog, type: type, name: str = None) -> None:
    
    """ Assigns the ExtendedSelection mode to a target child of a dialog. """

    target = dialog.findChild(type, name)

    if target != None:
        target.setSelectionMode(QAbstractItemView.ExtendedSelection)