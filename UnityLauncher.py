import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'generated'))

if(os.path.basename(sys.executable) == "UnityLauncher.exe"):
    applicationPath = os.path.dirname(sys.executable)
else:
    applicationPath = os.path.abspath(".")

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from generated.UnityLauncherGenerated import Ui_MainWindow
from src.Config import Config
from src.ProjectData import ProjectData
from src.SettingsDialog import SettingsDialog

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
        if(item == None):
            return
        projectData = item.data(0, QtCore.Qt.UserRole)
        print(projectData.name)
        menu = QtWidgets.QMenu()
        menu.addAction("Set Description", lambda: projectData.setDescription())
        menu.addAction("Set Icon", lambda: projectData.setIcon())
        menu.addAction("Delete Project", lambda: projectData.deleteProject())
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
        settings = SettingsDialog(self.centralwidget)
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