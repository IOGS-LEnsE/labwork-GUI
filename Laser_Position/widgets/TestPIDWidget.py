# -*- coding: utf-8 -*-
"""Laser Position Control Interface

PID Test Page

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
    >>> python TestPIDWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal

from widgets.NucleoSerialConnectionWidget import NucleoSerialConnectionWidget

"""
"""
class TestPIDWidget(QWidget):

    pid_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        """

        """
        super().__init__()
        self.parent = parent

        self.layout = QVBoxLayout()
        # Title label
        self.title_label = QLabel('NOT YET IMPLEMENTED')
        self.title_label.setStyleSheet("font-size: 16px; text-align: center; color:blue;")
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
        self.intro = TestPIDWidget()

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