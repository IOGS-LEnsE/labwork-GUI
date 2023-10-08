# Libraries to import
import sys
import os
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtGui import QIcon

# -------------------------------------------------------------------------------------------------------

# Colors
"""
Colors :    Green  : #c5e0b4
            Blue   : #4472c4
            Orange : #c55a11
            Beige  : #fff2cc
            Grey1  : #f2f2f2
            Grey2  : #bfbfbf
"""


# -------------------------------------------------------------------------------------------------------

class Parameters_AutoMode_Window(QWidget):
    """
    Widget used to parameter our AutoMode.

    Args:
        QWidget (class): QWidget can be put in another widget and / or window.
    """

    def __init__(self, default_path=None):
        """
        Initialisation of the Widget.
        """
        super().__init__()

        if default_path is None:
            self.path = os.path.expanduser('~')
        else:
            self.path = default_path
        self.setWindowTitle("Automatic Mode Parameters Window")
        self.setWindowIcon(QIcon("IOGSLogo.jpg"))

        # Creating and adding widgets into our layout
        layout = QGridLayout()

        self.directoryLabel = QLabel("Directory")
        self.directoryLabel.setStyleSheet("border-style: none;")

        self.directoryPushButton = QPushButton("Directory")
        self.directoryPushButton.setStyleSheet("background: #c5e0b4; color: black;")

        self.z0_displacement_label = QLabel('Init Z value / Z0 (um)')
        self.z0_displacement_label.setStyleSheet("border-style: none;")
        self.z0_displacement_line = QLineEdit()
        self.z0_displacement_line.setStyleSheet("background: white; color: black;")

        self.z_final_label = QLabel("Final Z value /Zf (um)")
        self.z_final_label.setStyleSheet("border-style: none;")
        self.z_final_line = QLineEdit()
        self.z_final_line.setStyleSheet("background: white; color: black;")

        self.z_step_label = QLabel("Z Step (nm)")
        self.z_step_label.setStyleSheet("border-style: none;")
        self.z_step_line = QLineEdit()
        self.z_step_line.setStyleSheet("background: white; color: black;")

        self.saveParametersPushButton = QPushButton("Save Parameters")
        self.saveParametersPushButton.setStyleSheet("background: #c5e0b4; color: black;")

        layout.addWidget(self.directoryLabel, 0, 0, 1, 2)  # row = 0, column = 0, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.directoryPushButton, 0, 2, 1, 2)  # row = 0, column = 2, rowSpan = 1, columnSpan = 2
        layout.addWidget(self.z0_displacement_label, 1, 0, 1, 2)
        layout.addWidget(self.z0_displacement_line, 1, 3, 1, 1)
        layout.addWidget(self.z_final_label, 2, 0, 1, 2)
        layout.addWidget(self.z_final_line, 2, 3, 1, 1)
        layout.addWidget(self.z_step_label, 3, 0, 1, 2)
        layout.addWidget(self.z_step_line, 3, 3, 1, 1)
        layout.addWidget(self.saveParametersPushButton, 4, 0, 1, 2)

        self.setLayout(layout)

    def setEnabled(self, enabled):
        """
        Method used to set the style sheet of the widget, if he is enable or disable.

        Args:
            enabled (bool): enable or disable.
        """
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet("background-color: #4472c4; border-radius: 10px; border-width: 1px;"
                               "border-color: black; padding: 6px; font: bold 12px; color: white;"
                               "text-align: center; border-style: solid;")
            self.directoryPushButton.setStyleSheet(
                "background: #7fadff; border-style: solid; border-width: 1px; font: bold; color: black")
            self.saveParametersPushButton.setStyleSheet(
                "background: #7fadff; border-style: solid; border-width: 1px; font: bold; color: black")

        else:
            self.setStyleSheet("background-color: #bfbfbf; border-radius: 10px; border-width: 1px;"
                               "border-color: black; padding: 6px; font: bold 12px; color: white;"
                               "text-align: center; border-style: solid;")
            self.directoryPushButton.setStyleSheet(
                "background: white; border-style: solid; border-width: 1px; font: bold; color: black")
            self.saveParametersPushButton.setStyleSheet(
                "background: white; border-style: solid; border-width: 1px; font: bold; color: black")


# -------------------------------------------------------------------------------------------------------

# Launching as main for tests
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Parameters_AutoMode_Window()
    window.show()

    sys.exit(app.exec())
