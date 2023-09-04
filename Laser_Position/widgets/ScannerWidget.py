# -*- coding: utf-8 -*-
"""Laser Position Control Interface

Scanner manual control Widget

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2023/09/01


Authors
-------
    Julien VILLEMEJANE

Use
---
    >>> python ScannerWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QLabel, QSlider
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import pyqtSignal, Qt

from TargetWidget import TargetWidget

# Global Constants
ACTIVE_COLOR = "#45B39D"
INACTIVE_COLOR = "#AF7AC5"

valid_style = "background:" + ACTIVE_COLOR + "; color:white; font-weight:bold;"
not_style = "background:" + INACTIVE_COLOR + "; color:white; font-weight:bold;"
active_style = "background:orange; color:white; font-weight:bold;"
no_style = "background:gray; color:white; font-weight:none;"
title_style = "background:darkgray; color:white; font-size:15px; font-weight:bold;"

class ScannerWidget(QWidget):
    """
        Widget used to control 2 axis scanners.
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
    actuator_signal = pyqtSignal(str)

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
        self.title_label = QLabel('Scanner Manual Control')
        self.title_label.setStyleSheet(title_style)
        self.control_layout.addWidget(self.title_label)

        self.layout.addWidget(self.control_widget, 0, 0)

        self.camera_widget = QWidget()
        self.camera_widget.setStyleSheet('background-color:lightgray;')
        self.layout.addWidget(self.camera_widget, 0, 1)

        self.widget_target_scan = QWidget()
        self.layout_target_scan = QGridLayout()
        self.widget_target_scan.setLayout(self.layout_target_scan)

        # X axis
        self.slider_x_ratio = 10.0
        self.slider_x = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_x.sliderMoved.connect(self.update_position)
        self.slider_x_label = QLabel('X = 0')
        self.slider_x.setMinimum(-100)
        self.slider_x.setMaximum(100)
        self.slider_x.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_x.setTickInterval(10)
        self.layout_target_scan.addWidget(self.slider_x_label, 1, 0)
        self.layout_target_scan.addWidget(self.slider_x, 0, 0)

        self.pos_x_dec1 = QPushButton('X-1')
        self.pos_x_zero = QPushButton('X=0')
        self.pos_x_upd1 = QPushButton('X+1')
        self.pos_x_dec1.clicked.connect(self.update_position)


        self.layout.addWidget(self.widget_target_scan, 1, 0)

        self.target_phd = TargetWidget()
        self.layout.addWidget(self.target_phd, 1, 1)

        self.setLayout(self.layout)


    def update_position(self, e):
        self.slider_x_label.setText('X = '+str(self.slider_x.value()/self.slider_x_ratio))
        self.slider_x_label.adjustSize()


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

# Colors
darkslategray = QColor(47, 79, 79)
gray = QColor(128, 128, 128)
lightgray = QColor(211, 211, 211)
fuschia = QColor(255, 0, 255)


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
        self.intro = ScannerWidget()

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
