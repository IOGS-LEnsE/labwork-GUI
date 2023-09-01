# -*- coding: utf-8 -*-
"""
2D Laser Position Control with PID controller.

Control with Nucleo L476RG

----------------------------------------------------------------------------
Co-Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-07-24
"""

from SupOpNumTools.drivers import SerialConnect

class LaserPID:
    """
    Class for Laser PID Control hardware interface
    Based on STM Nucleo L476RG

    List of commands
    ----------------
        Stop / Init
            O_!\r\n
            No return

        Alignment position
            A_!\r\n
            A_Xvalue_Yvalue_!\r\n   Xvalue and Yvalue are double values  (x2 for each channel)

        Servomotor position
            M_Xpos_Ypos_!\r\n

    """

    def __init__(self, baudrate = 115200):
        """

        Args:
            baudrate:
        """
        self.hardware_connection = SerialConnect(baudrate)

    def connect_to_hardware(self):
        print('connection')

    def send_stop(self):
        print('send_stop')