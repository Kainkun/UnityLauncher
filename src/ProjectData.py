import os
import shutil
import subprocess
import time

from pathlib import Path
from PIL import Image
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from send2trash import send2trash

from src.CustomSortTreeWidgetItem import CustomSortTreeWidgetItem


class ProjectData:
    def openProject(self):
        if self.unityPath == None:
            print("Could not find valid unity editor path")
            return False
        self.timeSinceModifiedDisplay = "Just now!"
        self.secondsSinceModified = 0
        self.rowWidget.setText(3, self.timeSinceModifiedDisplay)
        subprocess.Popen([self.unityPath, '-projectPath', self.projectPath])
        return True

    def buildLinux64(self):
        self.__buildHelper("-buildLinux64Player", "Linux 64", "Application")

    def buildOSXUniversal(self):
        self.__buildHelper("-buildOSXUniversalPlayer", "OSX", "Application.app")

    def buildWindows64(self):
        self.__buildHelper("-buildWindows64Player", "Windows 64", "Application.exe")

    def buildWindows32(self):
        self.__buildHelper("-buildWindowsPlayer", "Windows 32", "Application.exe")

    # TODO: double check the path stuff here is OS independent, add more options for building (like different platforms, maybe one of each, automate every night ect.)
    # TODO: make a better loading window while the build is processing so it doesnt look like we just crashed [ADDENDUM] now its non-blocking, but we probably want
    # TODO: ... a better way to keep track of the current build jobs - maybe go back to the blocking method and throw it on a new thread?
    def __buildHelper(self, buildType, buildFolderName, applicationName):
        
        buildPath = os.path.join(self.projectPath, 'Builds', 'UnityLauncherBuild', buildFolderName)
        applicationPath = os.path.join(buildPath, applicationName)

        if not os.path.exists(buildPath):
            os.makedirs(buildPath)

        subprocess.Popen([self.unityPath, '-projectPath', self.projectPath, '-batchmode', buildType, applicationPath, '-quit'])

    def setDescription(self, text=None):
        if not text:
            text = ProjectData.getDescriptionDialogue(self.parent, self)
        if text:
            self.description = text
            self.rowWidget.setText(2, text)
            with open(self.descriptionFilePath, "w") as file:
                file.write(text)

    @staticmethod
    def getDescriptionDialogue(parent, projectData=None):
        dialog = QtWidgets.QInputDialog(parent)
        dialog.setOptions(QtWidgets.QInputDialog.UsePlainTextEditForTextInput)
        if projectData and projectData.name:
            dialog.setWindowTitle(projectData.name + " Description")
        else:
            dialog.setWindowTitle("Description")
        dialog.setLabelText("Edit Description")
        if projectData:
            dialog.setTextValue(projectData.description)
        dialog.setWindowFlag(
            QtCore.Qt.WindowType.WindowContextHelpButtonHint, False)
        dialog.setInputMode(QtWidgets.QInputDialog.InputMode.TextInput)
        dialog.setSizeGripEnabled(True)
        dialog.resize(600, 200)
        ok = dialog.exec_()
        text = dialog.textValue()
        if ok:
            return text
        return None

    def setIcon(self, img=None):

        if not img:
            img = ProjectData.getIconDialogue()
        if not img:
            return
        if self.iconExists:
            send2trash(self.iconPath)
        img.save(self.iconPath)

        self.iconLabel.setPixmap(QtGui.QPixmap(self.iconPath))
        self.rowWidget.setSortData(0, self.iconPath)

    @staticmethod
    def getIconDialogue():
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        selected = fileDialog.exec()
        if selected:
            file = fileDialog.selectedFiles()[0]

            img = Image.open(file)

            basewidth = 300
            baseHeight = 300

            if img.width < img.height:
                wpercent = (basewidth / float(img.width))
                hsize = int((float(img.height) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            else:
                hpercent = (baseHeight / float(img.height))
                wsize = int((float(img.width) * float(hpercent)))
                img = img.resize((wsize, baseHeight), Image.ANTIALIAS)

            img = img.crop(((img.width - basewidth) // 2,
                            (img.height - baseHeight) // 2,
                            (img.width + basewidth) // 2,
                            (img.height + baseHeight) // 2))
            return img
        return None

    def showInExplorer(self):
        subprocess.Popen(
            r'explorer /select,"{0}"'.format(self.projectPath).replace('/', '\\'))

    def EditorScriptsUpToDate(self):
        editorScriptsFolder = os.path.join(
            self.projectPath, "Assets\\Editor\\UnityLauncher")

        MenuItems = os.path.join(editorScriptsFolder, "MenuItems.cs")
        TextureScale = os.path.join(editorScriptsFolder, "TextureScale.cs")

        if not os.path.exists(MenuItems):
            return 1

        if not os.path.exists(TextureScale):
            return 1

        expectedFirstLine = r"//" + os.environ["UNITY_LAUNCHER_VERSION"]

        with open(MenuItems) as f:
            first_line = f.readline()
            menuItemsUptoDate = first_line.startswith(expectedFirstLine)

        with open(TextureScale) as f:
            first_line = f.readline()
            textureScaleUptoDate = first_line.startswith(expectedFirstLine)

        if menuItemsUptoDate and textureScaleUptoDate:
            return 0
        else:
            return 2

    def AddEditorScripts(self):
        editorScriptsFolder = os.path.join(
            self.projectPath, "Assets\\Editor\\UnityLauncher")
        Path(editorScriptsFolder).mkdir(parents=True, exist_ok=True)

        MenuItems = os.path.join(
            os.environ["UNITY_LAUNCHER_APPLICATION_PATH"], "unityFiles\\UnityLauncher\\MenuItems.cs")

        TextureScale = os.path.join(
            os.environ["UNITY_LAUNCHER_APPLICATION_PATH"], "unityFiles\\UnityLauncher\\TextureScale.cs")

        shutil.copy(MenuItems, editorScriptsFolder)
        shutil.copy(TextureScale, editorScriptsFolder)

    def deleteProject(self):
        msgBox = QtWidgets.QMessageBox(self.parent)
        msgBox.setWindowTitle("Delete " + self.name)
        msgBox.setText(
            'Are you sure you want to delete "{0}"?\nIt will go to the recycle bin.'.format(self.name))
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        if msgBox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            send2trash(self.projectPath)
            index = self.parent.indexOfTopLevelItem(self.rowWidget)
            self.parent.takeTopLevelItem(index)

    def __init__(self, parent: QtWidgets.QTreeWidget, name: str, projectPath: str, unityPath: str, editorVersion: str):
        self.parent = parent
        self.name = name
        self.projectPath = projectPath.replace('/', '\\')
        self.unityPath = unityPath
        if self.unityPath:
            self.unityPath = self.unityPath.replace('/', '\\')
        self.editorVersion = editorVersion

        self.rowWidget = CustomSortTreeWidgetItem(parent)
        self.rowWidget.setData(0, QtCore.Qt.UserRole, self)

        #### NAME####
        self.rowWidget.setText(1, name)

        #### DESCRIPTION####

        # #For backwards compatibility. Will mess up your last modified order. Maybe look into MOVE command.
        # if(os.path.exists(os.path.join(self.projectPath, "desc.txt"))):
        #     os.rename(os.path.join(self.projectPath, "desc.txt"), os.path.join(self.projectPath, "description.txt"))

        self.descriptionFilePath = os.path.join(
            self.projectPath, "description.txt")
        self.descriptionExists = os.path.exists(self.descriptionFilePath)
        if self.descriptionExists:
            with open(self.descriptionFilePath) as descriptionFile:
                self.description = descriptionFile.read()
        else:
            self.description = ""

        self.rowWidget.setText(2, self.description)

        #### MODIFIED####
        lastModifiedEpic = os.path.getmtime(self.projectPath)
        self.secondsSinceModified = (time.time() - lastModifiedEpic)

        minutes = self.secondsSinceModified/60
        hours = minutes/60
        days = hours/24
        months = days/30
        years = days/365

        if years >= 1:
            self.timeSinceModifiedDisplay = str(round(years, 1)) + " years ago"
        elif months >= 1:
            if round(months) == 1:
                self.timeSinceModifiedDisplay = "a month ago"
            else:
                self.timeSinceModifiedDisplay = str(
                    round(months)) + " months ago"
        elif days >= 1:
            if round(days) == 1:
                self.timeSinceModifiedDisplay = "a day ago"
            else:
                self.timeSinceModifiedDisplay = str(round(days)) + " days ago"
        elif hours >= 1:
            if round(hours) == 1:
                self.timeSinceModifiedDisplay = "an hour ago"
            else:
                self.timeSinceModifiedDisplay = str(
                    round(hours)) + " hours ago"
        elif minutes >= 1:
            if round(minutes) == 1:
                self.timeSinceModifiedDisplay = "a minute ago"
            else:
                self.timeSinceModifiedDisplay = str(
                    round(minutes)) + " minutes ago"
        else:
            if round(self.secondsSinceModified) == 1:
                self.timeSinceModifiedDisplay = "a second ago"
            else:
                self.timeSinceModifiedDisplay = str(
                    round(self.secondsSinceModified)) + " seconds ago"

        self.rowWidget.setText(3, self.timeSinceModifiedDisplay)
        self.rowWidget.setSortData(3, self.secondsSinceModified)

        #### EDITOR VERSION####
        self.rowWidget.setText(4, self.editorVersion)

        #### ICON####
        self.iconLabel = QtWidgets.QLabel(parent)
        self.iconLabel.setMinimumSize(QtCore.QSize(150, 150))
        self.iconLabel.setMaximumSize(QtCore.QSize(150, 150))

        # # For backwards compatibility. Will mess up your last modified order.
        # original = os.path.join(self.projectPath, "icon.png")
        # new = os.path.join(self.projectPath, "icon.png")
        # if(os.path.exists(original)):
        #     img = Image.open(original)
        #     #img = img.convert('RGB')
        #     #img.thumbnail((300,300), Image.ANTIALIAS)

        #     basewidth = 300
        #     baseHeight = 300

        #     if(img.width < img.height):
        #         wpercent = (basewidth / float(img.width))
        #         hsize = int((float(img.height) * float(wpercent)))
        #         img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        #     else:
        #         hpercent = (baseHeight / float(img.height))
        #         wsize = int((float(img.width) * float(hpercent)))
        #         img = img.resize((wsize, baseHeight), Image.ANTIALIAS)

        #     img = img.crop(((img.width - basewidth) // 2,
        #                  (img.height - baseHeight) // 2,
        #                  (img.width + basewidth) // 2,
        #                  (img.height + baseHeight) // 2))

        #     send2trash(original)
        #     img.save(new)

        self.iconPath = os.path.join(self.projectPath, "icon.png")
        self.iconExists = os.path.exists(self.iconPath)
        if self.iconExists:
            self.iconLabel.setPixmap(QtGui.QPixmap(self.iconPath))
        else:
            self.iconLabel.setPixmap(QtGui.QPixmap(
                ":/images/UnityIconWhitePadded.png"))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("icon")

        # TODO: something really weird happens with the execution order involving this line of code below (136).
        # TODO: for some reason, it tries to start sorting when called, causing some invalid comparisons and an exception if everything else hasn't been set up.
        # TODO: Executing it after everything else has been initialized seems to fix the problem.
        parent.setItemWidget(self.rowWidget, 0, self.iconLabel)

        if self.iconExists:
            self.rowWidget.setSortData(0, self.iconPath)
        else:
            self.rowWidget.setSortData(0, "")

        parent.addTopLevelItem(self.rowWidget)
