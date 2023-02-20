from src.SettingsDialog import SettingsDialog
from src.ProjectData import ProjectData
from src.Config import Config
from generated.UnityLauncherGenerated import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import os
import sys

if os.path.basename(sys.executable) == "UnityLauncher.exe":
    # applicationPath = os.path.dirname(sys.executable)
    os.environ["UNITY_LAUNCHER_APPLICATION_PATH"] = os.path.dirname(
        sys.executable)
else:
    # applicationPath = os.path.abspath(".")
    os.environ["UNITY_LAUNCHER_APPLICATION_PATH"] = os.path.abspath(".")

os.environ["UNITY_LAUNCHER_VERSION"] = "v1.1"

# todo: move this free method somewhere else, with other common utilities?
# todo: this current implementation is window-specific, we want to add some os checking to change the location
def openLogs():
    localAppData = os.getenv("LOCALAPPDATA")
    logPath = f"{localAppData}\\Unity\\Editor\\Editor.log"
    os.startfile(logPath)

class LauncherMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args):
        QtWidgets.QMainWindow.__init__(self, *args)
        self.config: Config = Config()
        ui = UiImplement(self)
        ui.setupUi(self)
        x, y = self.config.getWindowPosition()
        w, h = self.config.getWindowSize()
        self.resize(QtCore.QSize(w, h))
        self.move(QtCore.QPoint(x, y))

    def closeEvent(self, closeEvent: QtGui.QCloseEvent):
        self.config.readChanges()
        self.config.setWindowSize((self.size().width(), self.size().height()))
        self.config.setWindowPosition((self.pos().x(), self.pos().y()))
        self.config.writeChanges()
        return super().closeEvent(closeEvent)


class UiImplement(Ui_MainWindow):

    def __init__(self, parent: LauncherMainWindow):
        super().__init__()
        self.parent = parent

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.addProjectsToList()
        self.projectTree.setColumnWidth(0, 150)
        self.projectTree.setColumnWidth(1, 200)
        self.projectTree.setColumnWidth(2, 600)
        self.projectTree.setColumnWidth(3, 200)
        self.projectTree.setColumnWidth(4, 200)
        self.projectTree.header().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.projectTree.sortItems(3, QtCore.Qt.SortOrder.AscendingOrder)
        self.projectTree.itemClicked.connect(
            lambda item: self.projectClicked(item))
        self.projectTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.projectTree.customContextMenuRequested.connect(
            lambda position: self.projectContextMenu(position))

        self.searchLineEdit.textChanged.connect(
            lambda text: self.searchBarChanged(text))

        # registering new menu-bar items
        self.menubar.addAction("Settings", lambda: self.__openSettings())
        self.menubar.addAction("Logs", lambda: openLogs())

        self.actionSet_All_Project_Icons.triggered.connect(
            lambda: self.setAllProjectIcons())
        self.actionSet_All_Project_Descriptions.triggered.connect(
            lambda: self.setAllProjectDescriptions())
        self.actionAdd_Editor_Scripts_to_All_Projects.triggered.connect(
            lambda: self.addEditorScriptsToAllProjects())

    def setAllProjectIcons(self):
        img = ProjectData.getIconDialogue()
        if not img:
            return
        for i in range(self.projectTree.invisibleRootItem().childCount()):
            projectData: ProjectData = self.projectTree.invisibleRootItem().child(i).data(0, QtCore.Qt.UserRole)
            projectData.setIcon(img)

    def setAllProjectDescriptions(self):
        text = ProjectData.getDescriptionDialogue(self.parent)
        if not text:
            return
        for i in range(self.projectTree.invisibleRootItem().childCount()):
            projectData: ProjectData = self.projectTree.invisibleRootItem().child(i).data(0, QtCore.Qt.UserRole)
            projectData.setDescription(text)

    def addEditorScriptsToAllProjects(self):
        for i in range(self.projectTree.invisibleRootItem().childCount()):
            projectData: ProjectData = self.projectTree.invisibleRootItem().child(i).data(0, QtCore.Qt.UserRole)
            projectData.AddEditorScripts()

    def addProjectsToList(self):
        self.parent.config.readChanges()
        for projectsFolderPath in self.parent.config.getProjectFolders():
            if not os.path.exists(projectsFolderPath):
                print('Error: Projects Folder "{0}" Does Not Exist'.format(
                    projectsFolderPath))
                continue

            for projectFolderName in os.listdir(projectsFolderPath):
                projectPath = os.path.join(
                    projectsFolderPath, projectFolderName)

                if not os.path.exists(projectPath):
                    print('Error: Project Folder "{0}" Does Not Exist'.format(
                        projectPath))
                    continue

                editorVersionPath = os.path.join(
                    projectPath, r"ProjectSettings\ProjectVersion.txt")
                if not os.path.exists(editorVersionPath):
                    print('Error: ProjectVersion.txt not found for "{0}"'.format(
                        projectFolderName))
                    continue
                with open(editorVersionPath) as versionPathFile:
                    firstline = versionPathFile.readline().rstrip()
                editorVersion = firstline.split(" ")[1]

                unityPath = None
                for unityEditorFolder in self.parent.config.getEditorFolders():
                    tryUnityPath = os.path.join(
                        unityEditorFolder, editorVersion, r"Editor\Unity.exe")
                    if os.path.exists(tryUnityPath):
                        unityPath = tryUnityPath
                        break

                ProjectData(self.projectTree, projectFolderName,
                            projectPath, unityPath, editorVersion)

    def projectClicked(self, item: QtWidgets.QTreeWidgetItem):
        success = item.data(0, QtCore.Qt.UserRole).openProject()
        if not success:
            msg = QtWidgets.QMessageBox(self.parent)
            # msg.setIcon(QtWidgets.QMessageBox.warning())
            msg.setText("Missing Unity Version")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setInformativeText('Unity version {0} does not exist in the settings folders'.format(
                item.data(0, QtCore.Qt.UserRole).editorVersion))
            msg.setWindowTitle("Error")
            msg.exec_()

    def projectContextMenu(self, position: QtCore.QPoint):
        item = self.projectTree.itemAt(position)
        if item == None:
            return
        projectData: ProjectData = item.data(0, QtCore.Qt.UserRole)
        menu = QtWidgets.QMenu(self.parent)
        menu.addAction("Set Icon", lambda: projectData.setIcon())
        menu.addAction("Set Description", lambda: projectData.setDescription())
        menu.addSeparator()
        menu.addAction("Show in Explorer",lambda: projectData.showInExplorer())
        menu.addAction("Build Window 64", lambda: projectData.buildWindows64())

        result = projectData.EditorScriptsUpToDate()
        if result == 1:
            menu.addSeparator()
            menu.addAction("Add Editor Scripts",
                           lambda: projectData.AddEditorScripts())
        elif result == 2:
            menu.addSeparator()
            menu.addAction("Update Editor Scripts",
                           lambda: projectData.AddEditorScripts())

        menu.addSeparator()
        menu.addAction("Delete Project", lambda: projectData.deleteProject())

        menu.exec(self.projectTree.mapToGlobal(position))

    def searchBarChanged(self, text: str):
        for index in range(self.projectTree.topLevelItemCount()):
            item = self.projectTree.topLevelItem(index)
            searchText = ''.join(filter(str.isalnum, text.lower()))
            itemText = ''.join(filter(str.isalnum, item.text(1).lower()))
            if searchText in itemText:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def __openSettings(self):
        settings = SettingsDialog(self.centralwidget)
        settings.exec()

        # After we close the settings, reload all of the projects.
        self.projectTree.clear()
        self.addProjectsToList()


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = LauncherMainWindow()
    MainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
