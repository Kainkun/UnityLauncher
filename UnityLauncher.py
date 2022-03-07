import os
import sys

from cv2 import FarnebackOpticalFlow

if(os.path.basename(sys.executable) == "UnityLauncher.exe"):
    applicationPath = os.path.dirname(sys.executable)
else:
    os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
    #os.system("pyrcc5 resource.qrc -o resource_rc.py")
    applicationPath = os.path.abspath(".")

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import subprocess
from UnityLauncherUI import Ui_MainWindow


class ProjectData:
    def openProject(self):
        if(self.unityPath == None):
            print("Could not find valid unity editor path")
            return

        subprocess.Popen([self.unityPath, '-projectPath', self.projectPath])
        #command = r'Start {0} -projectPath {1}'.format(self.unityPath, self.projectPath)
        #print(command)
        #os.system(command)
        
    def __init__(self, parent: QtWidgets.QTreeWidget, title: str, description: str, iconPath: str, projectPath: str, unityPath: str):
        self.title = title
        self.description = description
        self.iconPath = iconPath
        self.projectPath = projectPath
        self.unityPath = unityPath

        self.descriptionLabel = QtWidgets.QLabel(parent)
        self.descriptionLabel.setObjectName("description")
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setAutoFillBackground(True)
        self.descriptionLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.iconLabel = QtWidgets.QLabel(parent)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasWidthForHeight())
        # self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(100, 100))
        self.iconLabel.setMaximumSize(QtCore.QSize(100, 100))
        self.iconLabel.setText("")
        self.iconLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        if(iconPath == None):
            self.iconLabel.setPixmap(QtGui.QPixmap("Images/UnityIconWhite.png"))
        else:
            self.iconLabel.setPixmap(QtGui.QPixmap(iconPath))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("icon")
        self.titleLabel = QtWidgets.QLabel(parent)
        self.titleLabel.setObjectName("title")
        self.titleLabel.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.descriptionLabel.setText(description)
        self.titleLabel.setText(title)

        self.item = QtWidgets.QTreeWidgetItem(parent)
        self.item.setData(0, 0, self)

        parent.setItemWidget(self.item, 0, self.iconLabel)
        self.item.setText(0, iconPath)
        self.item.setForeground(0, QtGui.QColor(0,0,0,0))

        parent.setItemWidget(self.item, 1, self.titleLabel)
        self.item.setText(1, title)
        self.item.setForeground(1, QtGui.QColor(0,0,0,0))

        parent.setItemWidget(self.item, 2, self.descriptionLabel)
        self.item.setText(2, description)
        self.item.setForeground(2, QtGui.QColor(0,0,0,0))

        parent.addTopLevelItem(self.item)

class UiImplement(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def speak(self):
        self.titleLabel.setText("bazinga")

    def addProjectsToList(self):
        with open(os.path.join(applicationPath, r'Config\UnityProjectsFolders.txt')) as unityProjectsConfig:
            projectsFolderList = unityProjectsConfig.readlines()
            for i in range(len(projectsFolderList)):
                projectsFolderList[i] = projectsFolderList[i].replace("/", "\\").rstrip()
        with open(os.path.join(applicationPath, r'Config\UnityEditorsFolders.txt')) as unityEditorsConfig:
            unityEditorsFolderList = unityEditorsConfig.readlines()
            for i in range(len(unityEditorsFolderList)):
                unityEditorsFolderList[i] = unityEditorsFolderList[i].replace("/", "\\").rstrip()

        for projectsFolderPath in projectsFolderList:
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

                versionPath = os.path.join(projectPath, r"ProjectSettings\ProjectVersion.txt")
                if(not os.path.exists(versionPath)):
                    print('Error: ProjectVersion.txt not found for "{0}"'.format(projectFolderName))
                    continue
                with open(versionPath) as versionPathFile:
                    firstline = versionPathFile.readline().rstrip()
                version = firstline.split(" ")[1]

                unityPath = None
                for unityEditorFolder in unityEditorsFolderList:
                    tryUnityPath = os.path.join(unityEditorFolder, version, r"Editor\Unity.exe")
                    if(os.path.exists(tryUnityPath)):
                        unityPath = tryUnityPath
                        break
                
                ProjectData(self.projectTree, projectFolderName, description, iconPath, projectPath, unityPath)


    def openProjectClick(self, item: QtWidgets.QTreeWidgetItem):
        item.data(0, 0).openProject()
    
    def highlight(self, item: QtWidgets.QTreeWidgetItem):
        print("enter")
        widget = self.projectTree.itemWidget(item)
        widget.setStyleSheet("background-color: rgb(255,0,0);")

    def mouseMouse(self, event: QtGui.QMouseEvent):
        widget = self.projectTree.itemWidget(self.projectTree.itemAt(event.pos()))
        widget.setStyleSheet("background-color: rgb(255,0,0);")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.addProjectsToList()
        #self.projectTree.sortItems(0, QtCore.Qt.SortOrder.DescendingOrder)
        self.projectTree.setMouseTracking(True)
        #self.projectTree.itemEntered.connect(lambda item: self.highlight(item))
        #self.projectTree.mouseMoveEvent = lambda event: self.mouseMouse(event)
        self.projectTree.itemClicked.connect(lambda item: self.openProjectClick(item))

        self.testButton.clicked.connect(lambda: self.speak())
        #self.openButton.clicked.connect(lambda: OpenUnityProject())


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = UiImplement()
ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())
