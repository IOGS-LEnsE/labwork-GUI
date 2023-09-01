# -*- coding: utf-8 -*-
"""Laser Position Control Interface

Actuator Page

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
    >>> python ActuatorWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import pyqtSignal

# Global Constants
ACTIVE_COLOR = "#45B39D"
INACTIVE_COLOR = "#AF7AC5"

valid_style = "background:" + ACTIVE_COLOR + "; color:white; font-weight:bold;"
not_style = "background:" + INACTIVE_COLOR + "; color:white; font-weight:bold;"
active_style = "background:orange; color:white; font-weight:bold;"
no_style = "background:gray; color:white; font-weight:none;"
title_style = "background:darkgray; color:white; font-size:15px; font-weight:bold;"

class ActuatorWidget(QWidget):
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

        self.target = PhotodiodeTarget()
        self.layout.addWidget(self.target, 1, 0, 1, 2)

        self.setLayout(self.layout)


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


class PhotodiodeTarget(QWidget):
    """
    Graphical object to display photodiode position on a target.
    
    ...

    Attributes
    ----------
    pos_x : float
        position on X axis of the photodiode
    pos_y : float
        position on Y axis of the photodiode

    Methods
    -------

    """

    def __init__(self):
        """
        Initialization of the target.
        """
        super().__init__()
        self.pos_x = 10
        self.pos_y = -10

    def paintEvent(self, event):
        """

        Args:
            event:

        Returns:

        """
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        center_x = width // 2
        center_y = height // 2
        painter = QPainter(self)
        main_line = QPen(darkslategray)
        main_line.setWidth(5)
        painter.setPen(main_line)
        painter.drawLine(center_x, 5, center_x, height - 5)
        painter.drawLine(5, center_y, width - 5, center_y)
        second_line = QPen(gray)
        second_line.setWidth(1)
        painter.setPen(second_line)
        for ki in range(21):
            if ki != 10:
                painter.drawLine(5 + ki * (width - 10) // 20, 5, 5 + ki * (width - 10) // 20, height - 5)
                painter.drawLine(5, 5 + ki * (height - 10) // 20, width - 5, 5 + ki * (height - 10) // 20)
        photodiode_point = QPen(fuschia)
        photodiode_point.setWidth(3)
        painter.setBrush(QBrush(fuschia))
        painter.setPen(photodiode_point)
        pos_x_real = center_x + self.pos_x
        pos_y_real = center_y + self.pos_y
        painter.drawEllipse(pos_x_real - 10, pos_y_real - 10, 20, 20)
        painter.drawLine(pos_x_real - 20, pos_y_real - 20, pos_x_real + 20, pos_y_real + 20)
        painter.drawLine(pos_x_real + 20, pos_y_real - 20, pos_x_real - 20, pos_y_real + 20)

        # CHANGE RATIO !!

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
        self.pos_x = x
        self.pos_y = y
        self.update()

    def get_position(self):
        """
        Get the position of the photodiode

        Returns:
            x, y : float - corresponding to x and y axis position
        """
        return self.pos_x, self.pos_y


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
