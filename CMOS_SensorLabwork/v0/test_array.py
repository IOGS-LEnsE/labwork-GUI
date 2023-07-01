# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 21:06:07 2023

@author: Villou
"""

import numpy as np

arrayRaw = np.array([2051, 1053, 100, 200, 500, 3000, 300, 800, 1500], dtype=np.int16)

print(type(arrayRaw))
print(type(arrayRaw[0]))
print(arrayRaw.shape)


cameraFrame8bb = arrayRaw / (2**(12-8))
cameraFrame8b = cameraFrame8bb .astype(np.uint8)

cameraFrameRaw = np.reshape(arrayRaw, (3, 3, -1))
cameraFrame8b = np.reshape(cameraFrame8b, (3, 3, -1))

print(type(cameraFrameRaw))
print(type(cameraFrameRaw[0][0][0]))
print(cameraFrameRaw.shape)

print(type(cameraFrame8b))
print(type(cameraFrame8b[0][0][0]))
print(cameraFrame8b.shape)