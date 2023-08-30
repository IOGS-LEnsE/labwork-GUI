# -*- coding: utf-8 -*-
"""Laser Position Control Interface

Introduction Page

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2023/07/10


Authors
-------
    Julien VILLEMEJANE

Use
---
    >>> python IntroductionWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout 
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal

"""
"""
class IntroductionWidget(QWidget):

    intro_signal = pyqtSignal(str)
    
    def __init__(self):
        """

        """
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.title_label = QLabel('Laser Position Demonstration')
        self.layout.addWidget(self.title_label)
        
        self.setLayout(self.layout)
        
        
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
        self.intro = IntroductionWidget()
        
        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.intro)
        self.setCentralWidget(self.widget)


# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())