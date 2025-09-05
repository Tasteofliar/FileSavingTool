import os
import re
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
from . import saveToolfn

class ToolWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(ToolWindow, self).__init__(*args, **kwargs)
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
        self.load_sequences()
        self.seq_listWidget.currentItemChanged.connect(self.load_shots)
        self.shot_listWidget.currentItemChanged.connect(self.load_Department)

    def load_sequences(self):
        if os.path.exists(self.path):
            for seq in sorted(os.listdir(self.path)):
                full_path = os.path.join(self.path, seq)
                if os.path.isdir(full_path) and re.match(r"^seq\d+$", seq):
                    self.seq_listWidget.addItem(seq)

    def load_shots(self, current):
        self.shot_listWidget.clear()
        if current:
            seq_name = current.text()
            seq_path = os.path.join(self.path, seq_name)
            if os.path.exists(seq_path):
                for shot in sorted(os.listdir(seq_path)):
                    full_path = os.path.join(seq_path, shot)
                    if os.path.isdir(full_path) and re.match(r"^shot\d+$", shot):
                        self.shot_listWidget.addItem(shot)

    def load_Department(self, current):
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
        self.open_button = QPushButton('Open')
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.close)

        self.opt_layout.addWidget(self.save_button)
        self.opt_layout.addWidget(self.open_button)
        self.opt_layout.addWidget(self.cancel_button)

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

    ui = ToolWindow(parent = ptr)
    ui.show()