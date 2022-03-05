import os
os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
os.system("pyrcc5 resource.qrc -o resource_rc.py")

import sys
from UnityLauncherUI import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMouseEvent

class ClickableFrame(QFrame):
    def mouseReleaseEvent(self, event: QMouseEvent):
        print("clicked")
        return super().mouseReleaseEvent(event)


class UiImplement(Ui_MainWindow):

    def speak(self):
        self.titleLabel.setText("bazinga")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.testButton.clicked.connect(self.speak)

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = UiImplement()
ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())