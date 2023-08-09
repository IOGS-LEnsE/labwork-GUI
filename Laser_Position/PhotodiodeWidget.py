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
    >>> python PhotodiodeWidget.py
"""

# Libraries to import
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,  QVBoxLayout 
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import pyqtSignal


class PhotodiodeWidget(QWidget):

    intro_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.title_label = QLabel('Photodiode Response')
        self.layout.addWidget(self.title_label)
        
        self.target = PhotodiodeTarget()
        self.layout.addWidget(self.target)
        
        self.setLayout(self.layout)
        
        
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
    info(additional=""):
        Prints the person's name and age.    
    """
    
    def __init__(self):
        """
        Initialization of the target.
        """
        super().__init__()
        self.pos_x = 0
        self.pos_y = 0
    
    def paintEvent(self, event):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        center_x = width // 2
        center_y = height // 2
        painter = QPainter(self)
        main_line = QPen(darkslategray)
        main_line.setWidth(5)
        painter.setPen(main_line)
        painter.drawLine(center_x, 5, center_x, height-5)
        painter.drawLine(5, center_y, width-5, center_y)
        second_line = QPen(gray)
        second_line.setWidth(1)
        painter.setPen(second_line)
        for ki in range(21):
            if ki != 10:
                painter.drawLine(5 + ki*(width-10) // 20, 5, 5 + ki*(width-10) // 20, height-5)
                painter.drawLine(5, 5 + ki*(height-10) // 20, width-5, 5 + ki*(height-10) // 20)
        photodiode_point = QPen(fuschia)
        photodiode_point.setWidth(3)
        painter.setBrush(QBrush(fuschia))
        painter.setPen(photodiode_point)
        pos_x_real = center_x + self.pos_x
        pos_y_real = center_y + self.pos_y
        painter.drawEllipse(pos_x_real - 10, pos_y_real - 10, 20, 20)
        painter.drawLine(pos_x_real - 20, pos_y_real - 20, pos_x_real + 20, pos_y_real + 20)
        painter.drawLine(pos_x_real + 20, pos_y_real - 20, pos_x_real - 20, pos_y_real + 20)


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