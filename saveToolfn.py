import maya.cmds as cmds
import os

def fileSaving(new_name):
    current = cmds.file(q=True, sn=True)
    new_name = ()

    current_dir = os.path.dirname(current)
    cmds.file(rename= new_name)
    cmds.file(save=True, force=True, type="mayaAscii")
    print(new_name)