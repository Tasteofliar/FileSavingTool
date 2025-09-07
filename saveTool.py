import os
import re
from tkinter import dialog
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from . import saveToolfn

class toolWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(toolWindow, self).__init__(*args, **kwargs)
        self.s_window = None
        self.o_window = None
        self.setWindowTitle('Save Tool')
        self.resize(300,150)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.initMainWidgets()
        self.initButtonWidgets()

    def initMainWidgets(self):
        self.tool_widget = QWidget()
        self.tool_layout = QGridLayout()
        self.tool_widget.setLayout(self.tool_layout)
        self.main_layout.addWidget(self.tool_widget)

        #===seq list box===
        self.seq_label = QLabel('Sequence')
        self.seq_listWidget = QListWidget()

        #===shot list box===
        self.shot_label = QLabel('Shot')
        self.shot_listWidget = QListWidget()

        #===Department list box===
        self.department_label = QLabel('Department')
        self.department_combobox = QComboBox()
        self.department_combobox.addItem('select')

        #===Version list box===
        self.version_label = QLabel('Version')
        self.version_listWidget = QListWidget()
        self.version_listWidget.setMinimumSize(100,150)

        self.tool_layout.addWidget(self.seq_label,0,0)
        self.tool_layout.addWidget(self.seq_listWidget,1,0)
        self.tool_layout.addWidget(self.shot_label,0,1)
        self.tool_layout.addWidget(self.shot_listWidget,1,1)
        self.tool_layout.addWidget(self.department_label,0,2)       
        self.tool_layout.addWidget(self.department_combobox,1,2, alignment=Qt.AlignTop)
        self.tool_layout.addWidget(self.version_label,3,0)       
        self.tool_layout.addWidget(self.version_listWidget, 4, 0, 1, 3)

        self.path = r"C:\projects\PYSTD\work\shots"
        self.loadSequences()
        self.seq_listWidget.currentItemChanged.connect(self.loadShots)
        self.shot_listWidget.currentItemChanged.connect(self.loadDepartment)

    def loadSequences(self):
        if os.path.exists(self.path):
            for seq in sorted(os.listdir(self.path)):
                full_path = os.path.join(self.path, seq)
                if os.path.isdir(full_path) and re.match(r"^seq\d+$", seq):
                    self.seq_listWidget.addItem(seq)

    def loadShots(self, current):
        self.shot_listWidget.clear()
        if current:
            seq_name = current.text()
            seq_path = os.path.join(self.path, seq_name)
            if os.path.exists(seq_path):
                for shot in sorted(os.listdir(seq_path)):
                    full_path = os.path.join(seq_path, shot)
                    if os.path.isdir(full_path) and re.match(r"^shot\d+$", shot):
                        self.shot_listWidget.addItem(shot)

    def loadDepartment(self, current):
        self.department_combobox.clear()
        self.department_combobox.addItem('select')
        if current:
            seq_name = self.seq_listWidget.currentItem().text()
            shot_name = current.text()
            shot_path = os.path.join(self.path, seq_name, shot_name)
            if os.path.exists(shot_path):
                for dmp in sorted(os.listdir(shot_path)):
                    full_path = os.path.join(shot_path, dmp)
                    if os.path.isdir(full_path):
                        self.department_combobox.addItem(dmp)
                  
    def initButtonWidgets(self):
        self.opt_widget = QWidget()
        self.opt_layout = QHBoxLayout()
        self.opt_widget.setLayout(self.opt_layout)
        self.main_layout.addWidget(self.opt_widget)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.saveWindowPopup)
        self.open_button = QPushButton('Open')
        self.open_button.clicked.connect(self.openWindowPopup)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)
        
        self.opt_layout.addWidget(self.save_button)
        self.opt_layout.addWidget(self.open_button)
        self.opt_layout.addWidget(self.cancel_button)

    def saveWindowPopup(self):
        if self.s_window is None:
            self.s_window = saveWindow(parent = self)
        self.s_window.show()

    def openWindowPopup(self):
        if self.o_window is None:
            self.o_window = openWindow(parent = self)
        self.o_window.show()
 
class saveWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(saveWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Save')
        self.set_save_label = QLabel("Are you sure to save?")

        self.save_layout = QVBoxLayout()
        self.setLayout(self.save_layout)

        self.save_layout.addWidget(self.set_save_label)

        self.confirm_button = QPushButton('Confirm')
        self.close_button = QPushButton('Cancel')
        self.save_layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.save)
        self.save_layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close)

    def save(self):
        seq = self.parent().seq_listWidget.currentItem().text()
        shot = self.parent().shot_listWidget.currentItem().text()
        department = self.parent().department_combobox.currentText()
        base_path = self.parent().path

        save_path = saveToolfn.saveFile(seq, shot, department,base_path)

class openWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(openWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Open')
        self.set_open_label = QLabel("Are you sure to open?")

        self.open_layout = QVBoxLayout()
        self.setLayout(self.open_layout)

        self.open_layout.addWidget(self.set_open_label)

        self.confirm_button = QPushButton('Confirm')
        self.popup_close_button = QPushButton('Cancel')
        self.open_layout.addWidget(self.confirm_button)
        self.open_layout.addWidget(self.popup_close_button)
        self.popup_close_button.clicked.connect(self.close)

def close():
    ui.close()

def run():
    global ui
    try:
        ui.close()
    except:
        pass

    maya_ptr = omui.MQtUtil.mainWindow()
    ptr = wrapInstance(int(maya_ptr), QWidget)

    ui = toolWindow(parent = ptr)
    ui.show()