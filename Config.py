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

    __configData: typing.Dict = {}
    __configName: str = "config.json"
    __projectFoldersKey = "ProjectFolders"
    __editorFoldersKey = "EditorFolders"

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
            json.dump(self.__configData, configFile, indent=4, sort_keys=True)

    def readChanges(self):
        with open(self.__configName) as configFile:
            self.__configData = json.load(configFile)

    def __init__(self) -> None:

        """ Handles the serialization and deserialization of persistent data for the UnityLauncher. """

        if not os.path.exists(self.__configName):
            self.__configData = self.__createDefaultConfig()
            self.writeChanges()
                
        self.readChanges()

    def __createDefaultConfig(self) -> typing.Dict:

        """ Creates the default JSON structure for first-time users. """

        return {
            self.__projectFoldersKey : [],
            self.__editorFoldersKey : []
        }