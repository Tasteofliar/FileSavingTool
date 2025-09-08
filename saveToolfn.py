import os
import maya.cmds as cmds
import re

def getSceneFolder(base_path, seq, shot, department):
    return os.path.join(base_path, seq, shot, department, "maya", "scenes")

def getNextVersion(save_dir, seq, shot, department):
    versions = []
    if os.path.exists(save_dir):
        for file in os.listdir(save_dir):
            match = re.match(rf"{seq}_{shot}_{department}_v(\d+)\.(ma)$", file)
            if match:
                versions.append(int(match.group(1)))

    if not versions:
        return 1 
    return max(versions) + 1

def saveFile(seq, shot, department, base_path):
    save_dir = getSceneFolder(base_path, seq, shot, department)
    version_num = getNextVersion(save_dir, seq, shot, department)
    filename = f"{seq}_{shot}_{department}_v{version_num:03d}.ma"
    save_path = os.path.join(save_dir, filename)

    cmds.file(rename=save_path)
    cmds.file(save=True, type="mayaAscii")

def openFile(seq, shot, department, base_path, filename):
    scene_dir = getSceneFolder(base_path, seq, shot, department)
    file_path = os.path.join(scene_dir, filename)

    if os.path.exists(file_path):
        cmds.file(file_path, open=True, force=True)
