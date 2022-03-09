import os
import json
import typing

class Config():

    configData: typing.Dict = {}
    configName: str = "config.json"

    # Keys used for accessing and storing data in the JSON file.

    projectFoldersKey = "ProjectFolders"
    editorFoldersKey = "EditorFolders"

    def __init__(self) -> None:

        if not os.path.exists(self.configName):
            self.configData = self.__createDefaultConfig()
            self.writeChanges()
                
        self.readChanges()

    def __createDefaultConfig(self) -> typing.Dict:
        return {
            self.projectFoldersKey : [],
            self.editorFoldersKey : []
        }

    # Getter-Setter for Project Folders
    
    def setProjectFolders(self, folders: typing.List[str]) -> None:
        self.configData[self.projectFoldersKey] = folders

    def getProjectFolders(self) -> typing.List[str]:
        return self.configData[self.projectFoldersKey]

    # Getter-Setter for Editor Folders

    def setEditorFolders(self, folders: typing.List[str]) -> None:
        self.configData[self.editorFoldersKey] = folders

    def getEditorFolders(self) -> typing.List[str]:
        return self.configData[self.editorFoldersKey]

    # Serialization

    def writeChanges(self):
        with open(self.configName, mode = "w+") as configFile:
            json.dump(self.configData, configFile, indent=4, sort_keys=True)

    def readChanges(self):
        with open(self.configName) as configFile:
            self.configData = json.load(configFile)