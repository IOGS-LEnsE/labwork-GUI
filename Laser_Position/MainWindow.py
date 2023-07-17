# -*- coding: utf-8 -*-
"""Laser Position Control Interface

This GUI drives a 2 dimensionnal scanner and collects
data from a 4 quadrants photodiode to control the position of 
a Laser beam

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
    >>> python MainWindow.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtGui import QIcon
from MainMenu import MainMenu
from IntroductionWidget import IntroductionWidget

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
        self.setWindowIcon(QIcon('IOGS-LEnsE-logo.jpg'))
        # Variables

        # Define Window title
        self.setWindowTitle("Laser Position Control")
        self.setWindowIcon(QIcon('_inc/IOGS-LEnsE-logo.jpg'))
        self.setGeometry(50, 50, 1000, 700)
        
        # Main Layout
        self.main_widget = QWidget()
        self.main_layout = QGridLayout()
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 4)
        self.main_widget.setLayout(self.main_layout)
        
        # Left Main Menu
        self.main_menu = MainMenu()
        self.main_layout.addWidget(self.main_menu, 0, 0)
        
        # Graphical objects
        self.intro_widget = IntroductionWidget()
        self.main_layout.addWidget(self.intro_widget, 0, 1)
        
        self.setCentralWidget(self.main_widget)


# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
