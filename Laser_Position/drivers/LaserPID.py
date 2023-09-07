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
		
	def is_connected(self):
		pass
	
	def get_phd_xy(self):
		return 0, 0
	
	def set_scan_xy(self, x, y):
		pass
		
	def get_scan_xy(self):
		return 0, 0
		
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
        print('send_stop')

	def reset_scan(self):
		pass