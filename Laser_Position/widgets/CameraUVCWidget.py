# -*- coding: utf-8 -*-
"""Laser Position Control Interface

Camera insert

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2023/10/03


Authors
-------
    Julien VILLEMEJANE

Use
---
    >>> python CameraUVCWidget.py
"""

# Libraries to import
import sys
import cv2

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap


class CameraUVCWidget(QWidget):
    """
        Widget used to display 4-quadrants photodiode information.
        Children of QWidget - QWidget can be put in another widget and / or window
        ---
    """

    def __init__(self):
        """

        """
        super().__init__()

        self.camera_index = 0
        self.camera_cap = cv2.VideoCapture(self.camera_index, cv2.CAP_MSMF)

        
        # Elements for displaying camera
        self.camera_display = QLabel()
        self.frame_width = self.width()-30
        self.frame_height = self.height()-20


        self.layout = QGridLayout()

        # 

        self.setLayout(self.layout)

    def refresh(self):
        # Reshape of the frame to adapt it to the widget
        ret, self.camera_array = self.camera_cap.read()
        print(self.camera_array.shape)
        self.frame_width = self.width()-30
        self.frame_height = self.height()-20
        print(f'W={self.frame_width} / H={self.frame_height}')
        self.camera_disp2 = cv2.resize(self.camera_array,
                                     dsize=(self.frame_width, 
                                            self.frame_height), 
                                     interpolation=cv2.INTER_CUBIC)
        
        h, w, ch = self.camera_disp2.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(self.camera_disp2.data, w, h, 
                                      bytes_per_line, QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.frame_width, self.frame_height, 
                                        Qt.AspectRatioMode.KeepAspectRatio)
        pmap = QPixmap.fromImage(p)
        
        self.camera_display.setPixmap(pmap)

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
        self.intro = CameraUVCWidget()

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
    
    window.intro.refresh()

    sys.exit(app.exec())
