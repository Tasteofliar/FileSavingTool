import os
import maya.cmds as cmds

def getSceneFolder(base_path, seq, shot, department):
    return os.path.join(base_path, seq, shot, department, "maya", "scenes")

def saveFile(seq, shot, department, base_path):
    save_dir = getSceneFolder(base_path, seq, shot, department)

    filename = f"{seq}_{shot}_{department}.ma"
    save_path = os.path.join(save_dir, filename)

    cmds.file(rename=save_path)
    cmds.file(save=True, type="mayaAscii")  