import os
os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
#os.system("pyrcc5 resource.qrc -o resource_rc.py")

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from UnityLauncherUI import Ui_MainWindow


class ClickableFrame(QtWidgets.QFrame):
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        print("clicked")
        return super().mouseReleaseEvent(event)

class ProjectData:
    def openProject(self):
        print(r"{0} -projectPath {1}".format(self.unityPath, self.projectPath))
        os.system(r"{0} -projectPath {1}".format(self.unityPath, self.projectPath))
        
    def __init__(self, parent: QtWidgets.QWidget, layout: QtWidgets.QLayout, title: str, description: str, iconPath: str, projectPath: str, unityPath: str):
        self.title = title
        self.description = description
        self.iconPath = iconPath
        self.projectPath = projectPath
        self.unityPath = unityPath

        self.projectWidget = QtWidgets.QFrame(parent)
        #projectWidget.setFixedHeight(250)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(projectWidget.sizePolicy().hasHeightForWidth())
        #projectWidget.setSizePolicy(sizePolicy)
        #projectWidget.setMinimumSize(QtCore.QSize(0, 10))
        #projectWidget.setMaximumSize(QtCore.QSize(16777215, 120))
        self.projectWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.projectWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.projectWidget.setObjectName("projectsContents")
        self.projectWidgetLayout = QtWidgets.QGridLayout(self.projectWidget)
        self.projectWidgetLayout.setObjectName("projectsContentsLayout")
        self.spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.projectWidgetLayout.addItem(self.spacerItem, 0, 1, 2, 1)
        self.descriptionLabel = QtWidgets.QLabel(self.projectWidget)
        self.descriptionLabel.setObjectName("description")
        self.projectWidgetLayout.addWidget(self.descriptionLabel, 1, 3, 1, 1)
        self.openButton = QtWidgets.QPushButton(self.projectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openButton.sizePolicy().hasHeightForWidth())
        self.openButton.setSizePolicy(sizePolicy)
        self.openButton.setMinimumSize(QtCore.QSize(100, 0))
        self.openButton.setObjectName("openButton")
        self.projectWidgetLayout.addWidget(self.openButton, 0, 4, 2, 1)
        self.iconLabel = QtWidgets.QLabel(self.projectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMaximumSize(QtCore.QSize(100, 100))
        self.iconLabel.setText("")
        if(iconPath == None):
            self.iconLabel.setPixmap(QtGui.QPixmap("Images/UnityIcon.png"))
        else:
            self.iconLabel.setPixmap(QtGui.QPixmap(iconPath))
        self.iconLabel.setScaledContents(True)
        self.iconLabel.setObjectName("icon")
        self.projectWidgetLayout.addWidget(self.iconLabel, 0, 0, 2, 1)
        self.titleLabel = QtWidgets.QLabel(self.projectWidget)
        self.titleLabel.setObjectName("title")
        self.projectWidgetLayout.addWidget(self.titleLabel, 0, 3, 1, 1)

        self.descriptionLabel.setText(description)
        self.openButton.setText("Open")
        self.titleLabel.setText(title)

        layout.addWidget(self.projectWidget)

        self.openButton.clicked.connect(lambda: self.openProject())

class UiImplement(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.projectDatas = []

    def speak(self):
        self.titleLabel.setText("bazinga")

    def addProjectToList(self, title: str, description: str, iconPath: str, projectPath: str, unityPath: str):
        projectData = ProjectData(self.projectsContents, self.projectsContentsLayout, title, description, iconPath, projectPath, unityPath)
        self.projectDatas.append(projectData)

    def addProjectsToList(self, projectsFolderPath: str):
        if(not os.path.exists(projectsFolderPath)):
            print('Error: Project Folder "{0}" Does Not Exist'.format(projectFolderName))
            return
            
        for projectFolderName in os.listdir(projectsFolderPath):
            projectPath = os.path.join(projectsFolderPath, projectFolderName)

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
            unityPath = os.path.join(r"C:\Other\Unity\Editors", version, r"Editor\Unity.exe")
            
            self.addProjectToList(projectFolderName, description, iconPath, projectPath, unityPath)


    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.addProjectsToList(r"C:\Other\Unity\Projects")
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.projectsContentsLayout.addItem(spacer)

        self.testButton.clicked.connect(lambda: self.speak())
        #self.openButton.clicked.connect(lambda: OpenUnityProject())


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = UiImplement()
ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())
