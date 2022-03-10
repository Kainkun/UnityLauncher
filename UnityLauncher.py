import os
import sys

if(os.path.basename(sys.executable) == "UnityLauncher.exe"):
    applicationPath = os.path.dirname(sys.executable)
else:
    os.system("pyuic5 -x UI/UnityLauncher.ui -o Generated/UnityLauncherGenerated.py")
    #os.system("pyrcc5 resource.qrc -o resource_rc.py")
    applicationPath = os.path.abspath(".")

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import subprocess
import time
from Generated.UnityLauncherGenerated import Ui_MainWindow
from Settings import Settings
from Config import Config

class CustomSortTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __lt__( self, other ):
        if ( not isinstance(other, CustomSortTreeWidgetItem) ):
            return super(CustomSortTreeWidgetItem, self).__lt__(other)

        tree = self.treeWidget()
        if ( not tree ):
            column = 0
        else:
            column = tree.sortColumn()

        return self.sortData(column) < other.sortData(column)

    def __init__( self, *args ):
        super(CustomSortTreeWidgetItem, self).__init__(*args)
        self._sortData = {}

    def sortData( self, column ):
        return self._sortData.get(column, self.text(column))

    def setSortData( self, column, data ):
        self._sortData[column] = data


class ProjectData:
    def openProject(self):
        if(self.unityPath == None):
            print("Could not find valid unity editor path")
            return
        subprocess.Popen([self.unityPath, '-projectPath', self.projectPath])

    def setDescription(self):
        print("set description")

    def setIcon(self):
        print("set icon")
        
    def __init__(self, parent: QtWidgets.QTreeWidget, iconPath: str, name: str, description: str, editorVersion: str, unityPath: str, projectPath: str):
        self.iconPath = iconPath
        self.name = name
        self.description = description
        self.editorVersion = editorVersion
        self.unityPath = unityPath
        self.projectPath = projectPath

        self.rowWidget = CustomSortTreeWidgetItem(parent)
        self.rowWidget.setData(0, QtCore.Qt.UserRole, self)

        ####NAME####
        self.rowWidget.setText(1, name)


        ####DESCRIPTION####
        self.rowWidget.setText(2, description)


        ####MODIFIED####
        lastModifiedEpic = os.path.getmtime(self.projectPath)
        secondsSinceModified = (time.time() - lastModifiedEpic)

        minutes = secondsSinceModified/60
        hours = minutes/60
        days = hours/24
        months = days/30
        years = days/365

        if(years >= 1):
            timeSinceModifiedDisplay = str(round(years, 1))  + " years ago"
        elif(months >= 1):
            if(round(months) == 1):
                timeSinceModifiedDisplay = "a month ago"
            else:
                timeSinceModifiedDisplay = str(round(months))  + " months ago"
        elif(days >= 1):
            if(round(days) == 1):
                timeSinceModifiedDisplay = "a day ago"
            else:
                timeSinceModifiedDisplay = str(round(days))  + " days ago"
        elif(hours >= 1):
            if(round(hours) == 1):
                timeSinceModifiedDisplay = "an hour ago"
            else:
                timeSinceModifiedDisplay = str(round(hours))  + " hours ago"
        elif(minutes >= 1):
            if(round(minutes) == 1):
                timeSinceModifiedDisplay = "a minute ago"
            else:
                timeSinceModifiedDisplay = str(round(minutes))  + " minutes ago"
        else:
            if(round(secondsSinceModified) == 1):
                timeSinceModifiedDisplay = "a second ago"
            else:
                timeSinceModifiedDisplay = str(round(secondsSinceModified)) + " seconds ago"

        self.rowWidget.setText(3, timeSinceModifiedDisplay)
        self.rowWidget.setSortData(3, secondsSinceModified)


        ####EDITOR VERSION####
        self.rowWidget.setText(4, self.editorVersion)

        ####ICON####
        self.iconLabel = QtWidgets.QLabel(parent)
        self.iconLabel.setMinimumSize(QtCore.QSize(150, 150))
        self.iconLabel.setMaximumSize(QtCore.QSize(150, 150))
        if(iconPath == None):
            self.iconLabel.setPixmap(QtGui.QPixmap("Images/UnityIconWhitePadded.png"))
            iconPath = ""
        else:
            self.iconLabel.setPixmap(QtGui.QPixmap(iconPath))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("icon")

        # TODO: something really weird happens with the execution order involving this line of code below (136).
        # TODO: for some reason, it tries to start sorting when called, causing some invalid comparisons and an exception if everything else hasn't been set up.
        # TODO: Executing it after everything else has been initialized seems to fix the problem.
        parent.setItemWidget(self.rowWidget, 0, self.iconLabel)

        self.rowWidget.setSortData(0, iconPath)

        parent.addTopLevelItem(self.rowWidget)


class UiImplement(Ui_MainWindow):
    def speak(self):
        self.titleLabel.setText("bazinga")

    def addProjectsToList(self):
        config = Config()

        for projectsFolderPath in config.getProjectFolders():
            if(not os.path.exists(projectsFolderPath)):
                print('Error: Projects Folder "{0}" Does Not Exist'.format(projectsFolderPath))
                continue
                
            for projectFolderName in os.listdir(projectsFolderPath):
                projectPath = os.path.join(projectsFolderPath, projectFolderName)

                if(not os.path.exists(projectPath)):
                    print('Error: Project Folder "{0}" Does Not Exist'.format(projectPath))
                    continue

                descriptionFilePath = os.path.join(projectPath, "desc.txt")
                if(os.path.exists(descriptionFilePath)):
                    with open(descriptionFilePath) as descriptionFile:
                        description = descriptionFile.read()
                else:
                    description = ""

                iconPath = os.path.join(projectPath, "icon.png")
                if(not os.path.exists(iconPath)):
                    iconPath = None

                editorVersionPath = os.path.join(projectPath, r"ProjectSettings\ProjectVersion.txt")
                if(not os.path.exists(editorVersionPath)):
                    print('Error: ProjectVersion.txt not found for "{0}"'.format(projectFolderName))
                    continue
                with open(editorVersionPath) as versionPathFile:
                    firstline = versionPathFile.readline().rstrip()
                editorVersion = firstline.split(" ")[1]

                unityPath = None
                for unityEditorFolder in config.getEditorFolders():
                    tryUnityPath = os.path.join(unityEditorFolder, editorVersion, r"Editor\Unity.exe")
                    if(os.path.exists(tryUnityPath)):
                        unityPath = tryUnityPath
                        break
                
                ProjectData(self.projectTree, iconPath, projectFolderName, description, editorVersion, unityPath, projectPath)

    def projectClicked(self, item: QtWidgets.QTreeWidgetItem):
        item.data(0, QtCore.Qt.UserRole).openProject()

    def projectContextMenu(self, position: QtCore.QPoint):
        item = self.projectTree.itemAt(position)
        projectData = item.data(0, QtCore.Qt.UserRole)
        print(projectData.name)
        menu = QtWidgets.QMenu()
        menu.addAction("Set Description", lambda: projectData.setDescription())
        menu.addAction("Set Icon", lambda: projectData.setIcon())
        menu.exec(self.projectTree.mapToGlobal(position))

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.addProjectsToList()
        self.projectTree.setColumnWidth(0,150)
        self.projectTree.setColumnWidth(1,200)
        self.projectTree.setColumnWidth(2,600)
        self.projectTree.setColumnWidth(3,200)
        self.projectTree.setColumnWidth(4,200)
        self.projectTree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.projectTree.sortItems(3, QtCore.Qt.SortOrder.AscendingOrder)
        self.projectTree.itemClicked.connect(lambda item: self.projectClicked(item))
        self.projectTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.projectTree.customContextMenuRequested.connect(lambda position: self.projectContextMenu(position))

        self.testButton.clicked.connect(lambda: self.speak())
        self.SettingsButton.clicked.connect(lambda: self.__openSettings())

    def __openSettings(self):
        settings = Settings(self.centralwidget)
        settings.exec()
        
        # After we close the settings, reload all of the projects.
        self.projectTree.clear()
        self.addProjectsToList()
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiImplement()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()