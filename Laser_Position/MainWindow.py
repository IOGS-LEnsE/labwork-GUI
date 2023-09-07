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
from drivers.LaserPID import LaserPID


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
        self.nucleo_board = LaserPID()
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
        self.intro_widget = IntroductionWidget(self)
        self.intro_widget.intro_signal.connect(self.update_mode)
        self.main_layout.addWidget(self.intro_widget, 0, 1)
        self.photodiode_widget = EmptyWidget()
        self.scanner_widget = EmptyWidget()

        self.setCentralWidget(self.main_widget)
        self.main_timer.setInterval(200)

    def get_nucleo_board(self):
        return self.nucleo_board

    def get_photodiode_value(self):
        """
        Send photodiode position command 'A_!' to the control board.

        After the command is received by the controller, an acknowledgement is sent :
            'A_posX_posY_!'   where posX and posY are the position of the beam on the photodiode

        Returns:
            x, y :float
                x and y position of the photodiode
        """
        self.serial_link.send_data('A_!')
        while self.serial_link.is_data_waiting() is False:
            pass
        data = self.serial_link.read_data(self.serial_link.get_nb_data()).decode('ascii')
        data_split = data.split('_')
        if len(data_split) == 4:
            return int(float(data_split[1])), int(float(data_split[2]))
        else:
            return None, None

    def set_scanner_position(self, x, y):
        """
        Send moving command 'M_x_y_!' to the control board.

        After the command is received by the controller, an acknowledgement is sent :
            'M_x_y_posX_posY_!'   where posX and posY are the position of the beam on the photodiode

        Args:
            x: float
                position on X-axis to move the scanner
            y: float
                position on Y-axis to move the scanner

        Returns:
            x, y :float
                x and y position of the photodiode
        """
        data = 'M_' + str(x) + '_' + str(y) + '_!'
        self.serial_link.send_data(data)
        while self.serial_link.is_data_waiting() is False:
            pass
        data = self.serial_link.read_data(self.serial_link.get_nb_data()).decode('ascii')
        data_split = data.split('_')
        if len(data_split) == 6:
            return int(float(data_split[3])), int(float(data_split[4]))
        else:
            return None, None

    def timer_action(self):
        if self.mode == 'P':  # Photodiode manual response
            x_phd_value, y_phd_value = self.get_photodiode_value()
            if x_phd_value is not None:
                self.photodiode_widget.set_position(x_phd_value, y_phd_value)
            self.photodiode_widget.refresh_target()
        elif self.mode == 'A':  # Scanner manual control
            scanner_x, scanner_y = self.scanner_widget.get_scanner_position()
            x_phd_value, y_phd_value = self.set_scanner_position(scanner_x, scanner_y)
            if x_phd_value is not None:
                self.scanner_widget.set_position(x_phd_value, y_phd_value)
            self.scanner_widget.refresh_target()

    def update_layout(self, new_widget):
        count = self.main_layout.count()
        if count > 1:
            item = self.main_layout.itemAt(count - 1)
            old_widget = item.widget()
            old_widget.deleteLater()
            self.main_layout.addWidget(new_widget, 0, 1)

    def update_mode(self, e):
        if self.nucleo_board is not None and e != 'C':
            self.nucleo_board.send_stop()
        if e == 'C':
            print('COnnected')
            self.mode = 'C'
            self.main_timer.stop()
            self.main_menu.update_menu('C')
        elif e == 'P':  # photodiode
            self.mode = 'P'
            self.main_timer.stop()
            self.photodiode_widget = PhotodiodeWidget(self.camera)
            self.photodiode_widget.photodiode_signal.connect(self.update_photodiode)
            self.update_layout(self.photodiode_widget)
            self.main_timer.setInterval(100)
        elif e == 'A':  # actuator
            self.mode = 'A'
            self.scanner_widget = ScannerWidget()
            self.update_layout(self.scanner_widget)
            self.main_timer.setInterval(200)
            self.main_timer.start()

    def update_photodiode(self, e):
        if e == 'P_Start':
            self.main_timer.setInterval(100)
            self.main_timer.start()
            self.mode = 'P'
        elif e == 'P_Stop':
            self.serial_link.send_data('O')
            self.main_timer.stop()
            self.mode = 'O'


# -------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
