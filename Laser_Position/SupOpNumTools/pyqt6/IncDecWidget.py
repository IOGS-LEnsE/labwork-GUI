# -*- coding: utf-8 -*-
"""Increment and Decrement Widget to use in PyQt6 applications

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2023/09/04


Authors
-------
    Julien VILLEMEJANE

Use
---
    >>> python IncDecWidget.py
"""

import sys
import numpy

# Third pary imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit
from PyQt6.QtWidgets import (QHBoxLayout, QGridLayout, QVBoxLayout,
                    QLabel, QPushButton, QMessageBox, QCheckBox, QComboBox)
from PyQt6.QtCore import QTimer, pyqtSignal, Qt

from PyQt6.QtCore import Qt, pyqtSignal, QObject, QRect
from pyqtgraph import PlotWidget, plot, mkPen

styleH1 = "font-size:20px; padding:7px; color:Navy; border-top: 1px solid Navy;"
styleH = "font-size:18px; padding:4px; color:Navy; font-weight:bold;"
styleV = "font-size:14px; padding:2px; "


class IncDecWidget(QWidget):
    """
    IncDecWidget class to create a widget with two buttons to increase and decrease
    a value.
    Children of QWidget
    ---

    Attributes
    ----------

    Methods
    -------

    """

    updated = pyqtSignal(str)

    def __init__(self, name="", percent=False):
        super().__init__()

        ''' Global Values '''
        self.ratio_gain = 1.0
        self.real_value = 0.0
        self.enabled = True
        ''' Layout Manager '''
        self.main_layout = QGridLayout()
        ''' Graphical Objects '''
        self.name = QLabel(name)
        self.user_value = QLineEdit()
        self.name.setStyleSheet(styleH)
        self.user_value.setStyleSheet(styleH)

        self.units = ''
        self.units_label = QLabel('')

        self.inc_button = QPushButton('+ '+str(self.ratio_gain))
        self.inc_button.clicked.connect(self.increase_value)
        self.inc_button.setStyleSheet("background:#B41E5D; color:white; font-size:16px; font-weight:bold;")
        self.dec_button = QPushButton('- '+str(self.ratio_gain))
        self.dec_button.clicked.connect(self.decrease_value)
        self.dec_button.setStyleSheet("background:#2192B6;font-size:16px; font-weight:bold;")

        self.gain_combo = QComboBox()
        self.gain_combo.addItems(['0.001', '0.01', '0.1', '1', '10', '100', '1000'])
        self.gain_combo.setCurrentIndex(3)
        self.gain_combo.currentIndexChanged.connect(self.gain_changed)

        self.set_zero_button = QPushButton('Set to 0')
        self.set_zero_button.clicked.connect(self.clear_value)

        self.main_layout.setColumnStretch(0, 2) # Dec button
        self.main_layout.setColumnStretch(1, 2) # Name
        self.main_layout.setColumnStretch(2, 3) # Value
        self.main_layout.setColumnStretch(3, 1) # Units
        self.main_layout.setColumnStretch(4, 2) # Inc button
        self.main_layout.setColumnStretch(5, 3) # Gain

        ''' Adding GO into the widget layout '''
        self.main_layout.addWidget(self.dec_button, 0, 0)
        self.main_layout.addWidget(self.name, 0, 1)  # Position 1,0 / 3 cells
        self.main_layout.addWidget(self.user_value, 0, 2)  # Position 1,1 / 3 cells
        self.main_layout.addWidget(self.units_label, 0, 3)
        self.main_layout.addWidget(self.inc_button, 0, 4)
        self.main_layout.addWidget(self.gain_combo, 1, 4)
        self.main_layout.addWidget(self.set_zero_button, 1, 2)
        self.setLayout(self.main_layout)

        ''' Events '''
        # self.slider.valueChanged.connect(self.slider_changed)
        # self.name.clicked.connect(self.value_changed)
        self.set_value(self.real_value)
        self.update_display()

    def gain_changed(self):
        new_gain = self.gain_combo.currentText()
        self.inc_button.setText('+ '+new_gain )
        self.dec_button.setText('- '+new_gain )
        self.ratio_gain = float(new_gain)

    def increase_value(self):
        self.real_value += self.ratio_gain
        self.update_display()
        self.updated.emit('inc')

    def decrease_value(self):
        self.real_value -= self.ratio_gain
        self.update_display()
        self.updated.emit('dec')

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name.setText(name)

    def set_enabled(self, value):
        self.enabled = value
        self.inc_button.setEnabled(value)
        self.dec_button.setEnabled(value)
        self.user_value.setEnabled(value)

    def value_changed(self, event):
        value = self.user_value.text()
        value2 = value.replace('.', '', 1)
        value2 = value2.replace('e', '', 1)
        value2 = value2.replace('-', '', 1)
        if value2.isdigit():
            self.real_value = float(value)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(f"Not a number")
            msg.setWindowTitle("Not a Number Value")
            msg.exec()
            self.real_value = 0
            self.user_value.setText(str(self.real_value))
        self.update_display()

    def set_units(self, units):
        self.units = units
        self.update_display()

    def update_display(self):
        negative_nb = False
        if self.real_value < 0:
            negative_nb = True
            self.real_value = -self.real_value
        if self.real_value / 1000.0 >= 1:
            display_value = self.real_value / 1000.0
            display_units = 'k' + self.units
        elif self.real_value / 1e6 >= 1:
            display_value = self.real_value / 1e6
            display_units = 'M' + self.units
        else:
            display_value = self.real_value
            display_units = self.units
        self.units_label.setText(f'{display_units}')
        if negative_nb:
            display_value = -display_value
            self.real_value = -self.real_value
        display_value = numpy.round(display_value, 3)
        self.user_value.setText(f'{display_value}')

    def get_real_value(self):
        return self.real_value

    def set_value(self, value):
        self.real_value = value
        self.update_display()

    def set_gain(self, value):
        self.ratio_gain = value
        self.update_display()

    def clear_value(self):
        self.real_value = 0
        self.ratio_gain = 1.0
        self.gain_combo.setCurrentIndex(3)
        self.gain_changed()
        self.update_display()


# -----------------------------------------------------------------------------------------------
# Only for testing
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XY Chart")
        self.setGeometry(300, 300, 300, 150)

        self.centralWid = QWidget()
        self.layout = QVBoxLayout()

        self.incdec_widget = IncDecWidget()
        self.incdec_widget.set_units('')
        self.incdec_widget.set_name('X')
        self.layout.addWidget(self.incdec_widget)

        self.centralWid.setLayout(self.layout)
        self.setCentralWidget(self.centralWid)


# Launching as main for tests
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec())