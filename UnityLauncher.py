import os
os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
os.system("pyrcc5 resource.qrc -o resource_rc.py")

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *
import sys
from UnityLauncherUI import Ui_MainWindow


class ClickableFrame(QFrame):
    def mouseReleaseEvent(self, event: QMouseEvent):
        print("clicked")
        return super().mouseReleaseEvent(event)


def OpenUnityProject():
    unityPath = r"C:\Other\Unity\Editors\2020.3.22f1\Editor\Unity.exe"
    projectPath = r"C:\Other\Unity\Projects\DeletedMemories"
    os.system("{0} -projectPath {1}".format(unityPath, projectPath))


class UiImplement(Ui_MainWindow):

    def speak(self):
        self.titleLabel.setText("bazinga")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.testButton.clicked.connect(lambda: self.speak())
        self.openButton.clicked.connect(lambda: OpenUnityProject())


app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = UiImplement()
ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())
