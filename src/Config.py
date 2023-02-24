from collections import OrderedDict

import os
import json

class Config():
    """ 
        Handles the serialization and deserialization of persistent data for the UnityLauncher.

        - Functions:
            - writeChanges() -> None
            - readChanges() -> None
            - setWindowSize(tuple[int, int]) -> None
            - getWindowSize() -> tuple[int, int] 
            - setWindowPosition() -> None
            - getWindowPosition() -> tuple[int, int]
            - setProjectFolders(list[str]) -> None
            - setEditorFolders(list[str]) -> None
            - getProjectFolders() -> list[str]
            - getEditorFolders() -> list[str]

        - Notes:
            - Follows the MonoState pattern: https://wiki.c2.com/?MonostatePattern, so 
            keep in mind there is hidden static state associated with this class.
    """

    __configData: OrderedDict = {}
    __configName: str = "config.json"

    # KEYS
    __windowSizeKey = "LauncherWindowSize"
    __windowPositionKey = "LauncherWindowPosition"
    __projectFoldersKey = "ProjectFolders"
    __editorFoldersKey = "EditorFolders"

    # Getter-Setter for Window size

    def setWindowSize(self, size: tuple[int, int]) -> None:
        self.__configData[self.__windowSizeKey] = size

    def getWindowSize(self) -> tuple[int, int]:
        return self.__configData[self.__windowSizeKey]

    # Getter-Setter for Window position

    def setWindowPosition(self, position: tuple[int, int]) -> None:
        self.__configData[self.__windowPositionKey] = position

    def getWindowPosition(self) -> tuple[int, int]:
        return self.__configData[self.__windowPositionKey]

    # Getter-Setter for Project Folders

    def setProjectFolders(self, folders: list[str]) -> None:
        self.__configData[self.__projectFoldersKey] = folders

    def getProjectFolders(self) -> list[str]:
        return self.__configData[self.__projectFoldersKey]

    # Getter-Setter for Editor Folders

    def setEditorFolders(self, folders: list[str]) -> None:
        self.__configData[self.__editorFoldersKey] = folders

    def getEditorFolders(self) -> list[str]:
        return self.__configData[self.__editorFoldersKey]

    # Serialization

    def writeChanges(self):
        with open(self.__configName, mode="w+") as configFile:
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

    def __createDefaultConfig(self) -> OrderedDict:
        """ Creates the default JSON structure for first-time users. """

        d = OrderedDict()
        d[self.__windowSizeKey] = [830, 535]
        d[self.__windowPositionKey] = [1504, 767]
        d[self.__projectFoldersKey] = []
        d[self.__editorFoldersKey] = []
        return d
