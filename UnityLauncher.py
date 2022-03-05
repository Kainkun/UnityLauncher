import os
os.system("pyuic5 -x UnityLauncher.ui -o UnityLauncherUI.py")
os.system("pyrcc5 resource.qrc -o resource_rc.py")

import sys
from PyQt5.QtWidgets import *
from UnityLauncherUI import Ui_MainWindow

class UiImplement(Ui_MainWindow):
    def speak(self):
        self.label.setText("bazinga")

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.pushButton.clicked.connect(self.speak)

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = UiImplement()
ui.setupUi(MainWindow)

MainWindow.show()
sys.exit(app.exec_())