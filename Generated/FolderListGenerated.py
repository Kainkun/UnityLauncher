# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/FolderList.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FolderListWidget(object):
    def setupUi(self, FolderListWidget):
        FolderListWidget.setObjectName("FolderListWidget")
        FolderListWidget.resize(261, 151)
        self.GroupProjectFolders = QtWidgets.QGroupBox(FolderListWidget)
        self.GroupProjectFolders.setGeometry(QtCore.QRect(0, 0, 261, 151))
        self.GroupProjectFolders.setObjectName("GroupProjectFolders")
        self.FolderList = QtWidgets.QListWidget(self.GroupProjectFolders)
        self.FolderList.setGeometry(QtCore.QRect(10, 20, 241, 81))
        self.FolderList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.FolderList.setObjectName("FolderList")
        self.ButtonRemoveFolder = QtWidgets.QPushButton(self.GroupProjectFolders)
        self.ButtonRemoveFolder.setEnabled(False)
        self.ButtonRemoveFolder.setGeometry(QtCore.QRect(120, 110, 121, 31))
        self.ButtonRemoveFolder.setObjectName("ButtonRemoveFolder")
        self.ButtonAddFolder = QtWidgets.QPushButton(self.GroupProjectFolders)
        self.ButtonAddFolder.setGeometry(QtCore.QRect(18, 110, 91, 31))
        self.ButtonAddFolder.setObjectName("ButtonAddFolder")

        self.retranslateUi(FolderListWidget)
        QtCore.QMetaObject.connectSlotsByName(FolderListWidget)

    def retranslateUi(self, FolderListWidget):
        _translate = QtCore.QCoreApplication.translate
        FolderListWidget.setWindowTitle(_translate("FolderListWidget", "Form"))
        self.GroupProjectFolders.setTitle(_translate("FolderListWidget", "Folder List"))
        self.ButtonRemoveFolder.setText(_translate("FolderListWidget", "Remove Folder"))
        self.ButtonAddFolder.setText(_translate("FolderListWidget", "Add Folder"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FolderListWidget = QtWidgets.QWidget()
    ui = Ui_FolderListWidget()
    ui.setupUi(FolderListWidget)
    FolderListWidget.show()
    sys.exit(app.exec_())
