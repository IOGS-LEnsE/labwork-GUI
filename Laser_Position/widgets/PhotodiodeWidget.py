# -*- coding: utf-8 -*-
"""Laser Position Control Interface

Photodiode manual vizualisation

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
    >>> python PhotodiodeWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal
from SupOpNumTools.pyqt6.TargetWidget import TargetWidget

# Global Constants
ACTIVE_COLOR = "#45B39D"
INACTIVE_COLOR = "#AF7AC5"

valid_style = "background:" + ACTIVE_COLOR + "; color:white; font-weight:bold;"
not_style = "background:" + INACTIVE_COLOR + "; color:white; font-weight:bold;"
active_style = "background:orange; color:white; font-weight:bold;"
no_style = "background:gray; color:white; font-weight:none;"
title_style = "background:darkgray; color:white; font-size:15px; font-weight:bold;"

class PhotodiodeWidget(QWidget):
    """
        Widget used to display 4-quadrants photodiode information.
        Children of QWidget - QWidget can be put in another widget and / or window
        ---

        Attributes
        ----------
        layout : QLayout
            layout of the widget
        title_label : QLabel
            label to display informations
        target : PhotodiodeTarget
            widget to display photodiode position in a target
    """
    photodiode_signal = pyqtSignal(str)

    def __init__(self, camera=None):
        """

        """
        super().__init__()

        self.camera = camera

        self.layout = QGridLayout()

        # Control Panel
        self.control_widget = QWidget()
        self.control_layout = QVBoxLayout()
        self.control_widget.setLayout(self.control_layout)
        self.title_label = QLabel('Photodiode Response')
        self.title_label.setStyleSheet(title_style)
        self.control_layout.addWidget(self.title_label)
        self.control_start_ph = QPushButton('Start')
        self.control_start_ph.clicked.connect(self.start_action)
        self.control_layout.addWidget(self.control_start_ph)
        self.control_stop_ph = QPushButton('Stop')
        self.control_stop_ph.clicked.connect(self.stop_action)
        self.control_layout.addWidget(self.control_stop_ph)

        self.layout.addWidget(self.control_widget, 0, 0)

        self.camera_widget = QWidget()
        self.camera_widget.setStyleSheet('background-color:lightgray;')
        self.layout.addWidget(self.camera_widget, 0, 1)

        self.target = TargetWidget()
        self.layout.addWidget(self.target, 1, 0, 1, 2)

        self.setLayout(self.layout)

    def start_action(self):
        self.photodiode_signal.emit('P_Start')
        print('start')

    def stop_action(self):
        self.photodiode_signal.emit('P_Stop')
        print('stop')

    def set_position(self, x, y):
        """
        Set the position to display on the target

        Parameters
        ----------
        x : float
            position on x axis
        y : float
            position on y axis

        Returns:
            change the position on the graphical target
        """
        self.target.set_position(x, y)

    def get_position(self):
        """
        Get the position of the photodiode

        Returns:
            x, y : float - corresponding to x and y axis position
        """
        return self.target.get_position()

    def refresh_target(self):
        self.target.update()

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
        self.intro = PhotodiodeWidget()

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
