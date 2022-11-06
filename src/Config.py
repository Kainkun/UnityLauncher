from collections import OrderedDict

import os
import json
import typing

class Config():
    """ 
        Handles the serialization and deserialization of persistent data for the UnityLauncher.

        - Functions:
            - setProjectFolders(List[str]) -> None
            - setEditorFolders(List[str]) -> None
            - getProjectFolders() -> List[str]
            - getEditorFolders() -> List[str]
            - writeChanges() -> None
            - readChanges() -> None

        - Notes:
            - Follows the MonoState pattern: https://wiki.c2.com/?MonostatePattern, so 
            keep in mind there is hidden static state associated with this class.
    """

    __configData: typing.OrderedDict = {}
    __configName: str = "config.json"
    __windowSize = "LauncherWindowSize"
    __windowPosition = "LauncherWindowPosition"
    __projectFoldersKey = "ProjectFolders"
    __editorFoldersKey = "EditorFolders"

    # Getter-Setter for Window size

    def setWindowSize(self, size) -> None:
        self.__configData[self.__windowSize] = size

    def getWindowSize(self):
        return self.__configData[self.__windowSize]

    # Getter-Setter for Window position

    def setWindowPosition(self, position) -> None:
        self.__configData[self.__windowPosition] = position

    def getWindowPosition(self):
        return self.__configData[self.__windowPosition]

    # Getter-Setter for Project Folders
    
    def setProjectFolders(self, folders: typing.List[str]) -> None:
        self.__configData[self.__projectFoldersKey] = folders

    def getProjectFolders(self) -> typing.List[str]:
        return self.__configData[self.__projectFoldersKey]

    # Getter-Setter for Editor Folders

    def setEditorFolders(self, folders: typing.List[str]) -> None:
        self.__configData[self.__editorFoldersKey] = folders

    def getEditorFolders(self) -> typing.List[str]:
        return self.__configData[self.__editorFoldersKey]

    # Serialization

    def writeChanges(self):
        with open(self.__configName, mode = "w+") as configFile:
            json.dump(self.__configData, configFile, indent=4)

    def readChanges(self):
        with open(self.__configName) as configFile:
            self.__configData = json.load(configFile)

    def __init__(self) -> None:

        """ Handles the serialization and deserialization of persistent data for the UnityLauncher. """

        if not os.path.exists(self.__configName):
            self.__configData = self.__createDefaultConfig()
            self.writeChanges()
                
        self.readChanges()

    def __createDefaultConfig(self) -> typing.OrderedDict:

        """ Creates the default JSON structure for first-time users. """

        d = OrderedDict()
        d[self.__windowSize] = []
        d[self.__windowPosition] = []
        d[self.__projectFoldersKey] = []
        d[self.__editorFoldersKey] = []
        return d