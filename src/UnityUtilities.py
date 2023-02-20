import os
import platform

# TODO: This should be crossplatform, but someone needs to still test: OSX, Linux
def openLogs():

    currentSystem = platform.system()
    logPath = None

    if currentSystem == "Darwin": # mac / OSX
        logPath = "~/Library/Logs/Unity/Editor.log"

    elif currentSystem == "Windows":
        localAppData = os.getenv("LOCALAPPDATA")
        logPath = f"{localAppData}\\Unity\\Editor\\Editor.log"

    elif currentSystem == "Linux":
        logPath = "~/.config/unity3d/Editor.log"

    if logPath != None:
        os.startfile(logPath)