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
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer
from widgets.MainMenu import MainMenu
from IntroductionWidget import IntroductionWidget
from widgets.PhotodiodeWidget import PhotodiodeWidget
from widgets.EmptyWidget import EmptyWidget
from ScannerWidget import ScannerWidget

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
        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.timer_action)
        self.serial_link = None
        self.camera = None  # TO ADD for embedded USB camera - with opencv
        self.mode = 'O'

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
        self.main_menu.menu_signal.connect(self.update_mode)
        self.main_layout.addWidget(self.main_menu, 0, 0)
        
        # Graphical objects
        self.intro_widget = IntroductionWidget()
        self.intro_widget.intro_signal.connect(self.update_mode)
        self.main_layout.addWidget(self.intro_widget, 0, 1)
        self.photodiode_widget = EmptyWidget()
        self.scanner_widget = EmptyWidget()
        
        self.setCentralWidget(self.main_widget)
        self.main_timer.setInterval(200)

    def timer_action(self):
        if self.mode == 'P': # Photodiode manual response
            self.serial_link.send_data('A_!')
            while self.serial_link.is_data_waiting() is False:
                pass
            time.sleep(0.01)
            data = self.serial_link.read_data(self.serial_link.get_nb_data()).decode('ascii')
            data_split = data.split('_')
            self.photodiode_widget.set_position(int(float(data_split[1])), int(float(data_split[2])))
            self.photodiode_widget.refresh_target()
        elif self.mode == 'A': # Scanner manual control
            print('Scanner')

    def update_layout(self, new_widget):
        count = self.main_layout.count()
        if count > 1:
            item = self.main_layout.itemAt(count - 1)
            old_widget = item.widget()
            old_widget.deleteLater()
            self.main_layout.addWidget(new_widget, 0, 1)

    def update_mode(self, e):
        if e == 'C':
            self.main_timer.start()
            self.main_menu.update_menu('C')
            self.serial_link = self.intro_widget.get_serial_link()
        elif e == 'P':  # photodiode
            self.photodiode_widget = PhotodiodeWidget(self.camera)
            self.photodiode_widget.photodiode_signal.connect(self.update_photodiode)
            self.update_layout(self.photodiode_widget)
            self.main_timer.setInterval(100)
        elif e == 'A':  # actuator
            self.scanner_widget = ScannerWidget()
            self.update_layout(self.scanner_widget)
            self.main_timer.setInterval(200)


    def update_photodiode(self, e):
        if e == 'P_Start':
            self.main_timer.setInterval(100)
            self.mode = 'P'
        elif e == 'P_Stop':
            self.serial_link.send_data('O')
            self.mode = 'O'




# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
