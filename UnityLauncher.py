import os
os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
os.system("pyrcc5 resource.qrc -o resource_rc.py")

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys
from UnityLauncherUI import Ui_MainWindow


class ClickableFrame(QtWidgets.QFrame):
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        print("clicked")
        return super().mouseReleaseEvent(event)


def OpenUnityProject():
    unityPath = r"C:\Other\Unity\Editors\2020.3.22f1\Editor\Unity.exe"
    projectPath = r"C:\Other\Unity\Projects\DeletedMemories"
    os.system("{0} -projectPath {1}".format(unityPath, projectPath))


class UiImplement(Ui_MainWindow):

    def speak(self):
        self.titleLabel.setText("bazinga")

    def addProjectToList(self, title: str, description: str, path: str, icon):
        projectWidget = QtWidgets.QFrame(self.projectsContents)
        #projectWidget.setFixedHeight(250)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(projectWidget.sizePolicy().hasHeightForWidth())
        #projectWidget.setSizePolicy(sizePolicy)
        #projectWidget.setMinimumSize(QtCore.QSize(0, 10))
        #projectWidget.setMaximumSize(QtCore.QSize(16777215, 120))
        projectWidget.setFrameShape(QtWidgets.QFrame.Box)
        projectWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        projectWidget.setObjectName("projectsContents")
        projectWidgetLayout = QtWidgets.QGridLayout(projectWidget)
        projectWidgetLayout.setObjectName("projectsContentsLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        projectWidgetLayout.addItem(spacerItem, 0, 1, 2, 1)
        descriptionLabel = QtWidgets.QLabel(projectWidget)
        descriptionLabel.setObjectName("description")
        projectWidgetLayout.addWidget(descriptionLabel, 1, 3, 1, 1)
        openButton = QtWidgets.QPushButton(projectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(openButton.sizePolicy().hasHeightForWidth())
        openButton.setSizePolicy(sizePolicy)
        openButton.setMinimumSize(QtCore.QSize(100, 0))
        openButton.setObjectName("openButton")
        projectWidgetLayout.addWidget(openButton, 0, 4, 2, 1)
        icon = QtWidgets.QLabel(projectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(icon.sizePolicy().hasHeightForWidth())
        icon.setSizePolicy(sizePolicy)
        icon.setMaximumSize(QtCore.QSize(100, 100))
        icon.setText("")
        icon.setPixmap(QtGui.QPixmap(":/images/Images/UnityIcon.png"))
        icon.setScaledContents(True)
        icon.setObjectName("icon")
        projectWidgetLayout.addWidget(icon, 0, 0, 2, 1)
        titleLabel = QtWidgets.QLabel(projectWidget)
        titleLabel.setObjectName("title")
        projectWidgetLayout.addWidget(titleLabel, 0, 3, 1, 1)

        descriptionLabel.setText(description)
        openButton.setText("Open")
        titleLabel.setText(title)

        self.projectsContentsLayout.addWidget(projectWidget)


    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.addProjectToList("TestTitle", "This is the description", r"C:\Other\Unity\Projects\DeletedMemories", None)
        self.addProjectToList("Project Name", "This is another description", r"C:\Other\Unity\Projects\DeletedMemories", None)
        self.addProjectToList("Hello World", "This is the third description", r"C:\Other\Unity\Projects\DeletedMemories", None)
        self.addProjectToList("Heyo", "This is the last description", r"C:\Other\Unity\Projects\DeletedMemories", None)
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
