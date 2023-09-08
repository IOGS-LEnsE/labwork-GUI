# -*- coding: utf-8 -*-
"""
2D Laser Position Control with PID controller.

Control with Nucleo L476RG

----------------------------------------------------------------------------
Co-Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2023-07-24
"""

import time

from SupOpNumTools.drivers.SerialConnect import SerialConnect


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

    def __init__(self, baudrate=115200):
        """

        Args:
            baudrate:
        """
        self.hardware_connection = SerialConnect(baudrate)
        self.connected = False
        self.serial_port = None
        self.scan_x = 0
        self.scan_y = 0
        self.phd_x = 0
        self.phd_y = 0

    def set_serial_port(self, value):
        self.serial_port = value
        self.hardware_connection.set_serial_port(self.serial_port)

    def get_serial_ports_list(self):
        return self.hardware_connection.get_serial_port_list()

    def connect_to_hardware(self):
        self.connected = self.hardware_connection.connect()
        return self.connected

    def is_connected(self):
        return self.connected

    def get_phd_xy(self):
        self.hardware_connection.send_data('A_!')
        while self.hardware_connection.is_data_waiting() is False:
            pass
        nb_data = self.hardware_connection.get_nb_data_waiting()
        data = self.hardware_connection.read_data(nb_data).decode('ascii')
        data_split = data.split('_')
        if len(data_split) == 4:
            self.phd_x = float(data_split[1])
            self.phd_y = float(data_split[2])
        else:
            self.phd_x = None
            self.phd_y = None
        return self.phd_x, self.phd_y

    def set_scan_xy(self, x, y):
        self.scan_x = x
        self.scan_y = y
        data = 'M_' + str(x) + '_' + str(y) + '_!'
        self.hardware_connection.send_data(data)
        while self.hardware_connection.is_data_waiting() is False:
            pass
        nb_data = self.hardware_connection.get_nb_data_waiting()
        data = self.hardware_connection.read_data(nb_data).decode('ascii')
        data_split = data.split('_')
        if len(data_split) == 6:
            self.phd_x = float(data_split[3])
            self.phd_y = float(data_split[4])
        else:
            self.phd_x = None
            self.phd_y = None
        return self.phd_x, self.phd_y

    def get_scan_xy(self):
        return self.scan_x, self.scan_y

    def set_sampling_freq(self, fs):
        pass

    def set_open_loop_steps(self, x1, y1, x2, y2):
        pass

    def set_open_loop_samples(self, n):
        # Not yet implemented in Hardware
        pass

    def get_open_loop_data(self):
        pass

    def set_PID_params(self, Kx, Ky, Ix=0, Iy=0, Dx=0, Dy=0):
        pass

    def start_PID_control(self):
        pass

    def stop_PID_control(self):
        pass

    def send_stop(self):
        self.hardware_connection.send_data('O_!')

    def reset_scan(self):
        pass

    def check_connection(self):
        # Sending data to check the connection
        self.hardware_connection.send_data('C')
        cpt_time = 0
        while cpt_time < 10 and self.hardware_connection.is_data_waiting() is False:
            time.sleep(0.1)
            cpt_time += 1
        if self.hardware_connection.is_data_waiting() != 0:
            nb_data = self.hardware_connection.get_nb_data_waiting()
            data_received = self.hardware_connection.read_data(nb_data).decode('ascii')
            if data_received[0] == 'C':
                return True
            else:
                return False
        else:
            return False
