# -*- coding: utf-8 -*-
"""Laser Position Control Interface - Menu

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2023/07/15


Authors
-------
    Julien VILLEMEJANE

Use
---
    >>> python MainMenu.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

# Global Constants
ACTIVE_COLOR = "#45B39D"
INACTIVE_COLOR = "#AF7AC5"

valid_style = "background:" + ACTIVE_COLOR + "; color:white; font-weight:bold;"
not_style = "background:" + INACTIVE_COLOR + "; color:white; font-weight:bold;"
no_style = "background:gray; color:white; font-weight:none;"
title_style = "background:darkgray; color:white; font-size:15px; font-weight:bold;"

class MainMenu(QWidget):

    menu_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.steps = 0

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addStretch()
        
        self.menu_introduction_button = QPushButton('Introduction')
        self.menu_layout.addWidget(self.menu_introduction_button)
        self.menu_introduction_button.setEnabled(False)
        self.menu_introduction_button.setStyleSheet(valid_style)
        self.menu_layout.addStretch()
        
        self.menu_photodiode_button = QPushButton('Photodiode')
        self.menu_photodiode_button.clicked.connect(self.photodiode_action)
        self.menu_layout.addWidget(self.menu_photodiode_button)

        self.menu_actuator_button = QPushButton('Actuator')
        self.menu_layout.addWidget(self.menu_actuator_button)
        self.menu_actuator_button.setEnabled(False)
        self.menu_actuator_button.setStyleSheet(not_style)

        self.menu_PID_test_button = QPushButton('PID Test')
        self.menu_layout.addWidget(self.menu_PID_test_button)
        self.menu_PID_test_button.setEnabled(False)
        self.menu_PID_test_button.setStyleSheet(not_style)
        self.menu_layout.addStretch()

        self.menu_central_position_button = QPushButton('Central Position')
        self.menu_layout.addWidget(self.menu_central_position_button)
        self.menu_central_position_button.setEnabled(False)
        self.menu_central_position_button.setStyleSheet(not_style)

        self.menu_open_loop_button = QPushButton('Open Loop')
        self.menu_layout.addWidget(self.menu_open_loop_button)
        self.menu_open_loop_button.setEnabled(False)
        self.menu_open_loop_button.setStyleSheet(not_style)    
        self.menu_layout.addStretch()        

        self.menu_PID_button = QPushButton('PID Control')
        self.menu_layout.addWidget(self.menu_PID_button)
        self.menu_PID_button.setEnabled(False)
        self.menu_PID_button.setStyleSheet(not_style)
        self.menu_layout.addStretch()
        
        self.setLayout(self.menu_layout)
       
    def photodiode_action(self, event):
        print('Photodiode')

# -------------------------------

class MainWindow(QMainWindow):
    """
    Our main window.

    Args:
        QMainWindow (class): QMainWindow can contain several widgets.
    """
    def __init__(self):
        """
        Initialisation of the main Window.
        """
        super().__init__()
        self.menu = MainMenu()
        
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.menu)
        self.setCentralWidget(self.widget)


# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())