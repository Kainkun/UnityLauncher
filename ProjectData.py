import subprocess
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from CustomSortTreeWidgetItem import CustomSortTreeWidgetItem

class ProjectData:
    def openProject(self):
        if(self.unityPath == None):
            print("Could not find valid unity editor path")
            return
        self.timeSinceModifiedDisplay = "Just now!"
        self.secondsSinceModified = 0
        self.rowWidget.setText(3, self.timeSinceModifiedDisplay)
        subprocess.Popen([self.unityPath, '-projectPath', self.projectPath])

    def setDescription(self):
        print("set description")

    def setIcon(self):
        print("set icon")

    def deleteProject(self):
        print("delete project")
        
    def __init__(self, parent: QtWidgets.QTreeWidget, iconPath: str, name: str, description: str, editorVersion: str, unityPath: str, projectPath: str):
        self.parent = parent
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
        self.secondsSinceModified = (time.time() - lastModifiedEpic)

        minutes = self.secondsSinceModified/60
        hours = minutes/60
        days = hours/24
        months = days/30
        years = days/365

        if(years >= 1):
            self.timeSinceModifiedDisplay = str(round(years, 1))  + " years ago"
        elif(months >= 1):
            if(round(months) == 1):
                self.timeSinceModifiedDisplay = "a month ago"
            else:
                self.timeSinceModifiedDisplay = str(round(months))  + " months ago"
        elif(days >= 1):
            if(round(days) == 1):
                self.timeSinceModifiedDisplay = "a day ago"
            else:
                self.timeSinceModifiedDisplay = str(round(days))  + " days ago"
        elif(hours >= 1):
            if(round(hours) == 1):
                self.timeSinceModifiedDisplay = "an hour ago"
            else:
                self.timeSinceModifiedDisplay = str(round(hours))  + " hours ago"
        elif(minutes >= 1):
            if(round(minutes) == 1):
                self.timeSinceModifiedDisplay = "a minute ago"
            else:
                self.timeSinceModifiedDisplay = str(round(minutes))  + " minutes ago"
        else:
            if(round(self.secondsSinceModified) == 1):
                self.timeSinceModifiedDisplay = "a second ago"
            else:
                self.timeSinceModifiedDisplay = str(round(self.secondsSinceModified)) + " seconds ago"

        self.rowWidget.setText(3, self.timeSinceModifiedDisplay)
        self.rowWidget.setSortData(3, self.secondsSinceModified)


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