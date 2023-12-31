# -*- coding: utf-8 -*-
"""IDS Camera Control library.

/!\ Only for IDS USB 2.0 CMOS camera
Based on pyueye library

---------------------------------------
(c) 2023 - LEnsE - Institut d'Optique
---------------------------------------

Modifications
-------------
    Creation on 2021/01/01


Authors
-------
    Samuel GERENTE
    Victoire DE SALEON-TERRAS
    Flora SILBERZAN
    Martin COLLIGNON
    Hugo LASSIETTE
    Oscar BOUCHER
    Julien VILLEMEJANE

"""

# Standard libraries
from pyueye import ueye
import time


class uEye_ERROR(Exception):
    """
    
    """

    def __init__(self, ERROR_mode="uEye_ERROR"):
        self.ERROR_mode = ERROR_mode
        super().__init__(self.ERROR_mode)


def get_nb_of_cam():
    """
    Return the number of camera connected

    :return: Number of uEye camera connected
    """
    nb = ueye.INT()
    ret = ueye.is_GetNumberOfCameras(nb)
    if ret != ueye.IS_SUCCESS:
        raise uEye_ERROR("is_GetNumberOfCameras")
        return 0
    else:
        return nb.value


def get_cam_list():
    """
    Return the list containing the ID, serial number and name of all cameras connected

    :return: list build like that [[cam1_id, cam1_ser_no, cam1_name], ... ]
    """
    nb_cam = get_nb_of_cam()
    if nb_cam > 0:
        cam_list = ueye.UEYE_CAMERA_LIST()
        cam_list.dwCount = get_nb_of_cam()

        ret = ueye.is_GetCameraList(cam_list)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_GetCameraList")
            return []
        else:
            cams_info = []
            for i in range(0, cam_list.dwCount.value):
                cam = cam_list.uci[i]

                cam_id = cam.dwCameraID
                cam_ser_no = cam.SerNo.decode('utf-8')
                cam_name = cam.FullModelName.decode('utf-8')

                cams_info.append([cam_id.value, cam_ser_no, cam_name])

            return cams_info
    else:
        return []


# -------------------------------------------------------------------------------------------------------

class uEyeCamera:
    def __init__(self, cam_id=0):
        self.h_cam = ueye.HIDS(cam_id)
        self.nBitsPerPixel = ueye.INT()
        self.colormode = None
        self.MemID = ueye.int()
        self.pcImageMemory = ueye.c_mem_p()
        self.width = ueye.INT()
        self.height = ueye.INT()
        self.pitch = ueye.INT()

        self.init()
        self.ser_no, self.id = self.get_cam_info()
        self.width_max, self.height_max, self.cam_name, self.cam_pixel = self.get_sensor_info()

    def init(self):
        ret = ueye.is_InitCamera(self.h_cam, None)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_InitCamera")
        ret = ueye.is_ResetToDefault(self.h_cam)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_ResetToDefault")

    def get_cam_info(self):
        cam_info = ueye.CAMINFO()

        ret = ueye.is_GetCameraInfo(self.h_cam, cam_info)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_GetCameraInfo")
            return None, None
        else:
            ser_no = cam_info.SerNo.decode('utf-8')
            cam_id = cam_info.Select.value
            return ser_no, cam_id

    def get_sensor_info(self):
        sensor_info = ueye.SENSORINFO()

        ret = ueye.is_GetSensorInfo(self.h_cam, sensor_info)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_GetSensorInfo")
            return None, None, None, None
        else:
            max_width = sensor_info.nMaxWidth
            max_height = sensor_info.nMaxHeight
            name = sensor_info.strSensorName.decode('utf-8')
            pixel = sensor_info.wPixelSize.value
            return max_width, max_height, name, pixel

    def get_sensor_max_width(self):
        sensor_info = ueye.SENSORINFO()

        ret = ueye.is_GetSensorInfo(self.h_cam, sensor_info)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_GetSensorInfo")
            return None
        else:
            return sensor_info.nMaxWidth.value

    def get_sensor_max_height(self):
        sensor_info = ueye.SENSORINFO()

        ret = ueye.is_GetSensorInfo(self.h_cam, sensor_info)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_GetSensorInfo")
            return None
        else:
            return sensor_info.nMaxHeight.value

    def set_display_mode(self, mode):
        ret = ueye.is_SetDisplayMode(self.h_cam, mode)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_SetDisplayMode")

    def capture_video(self):
        """
        Start the FreeRun mode of the camera

        :return: No return
        """
        ret = ueye.is_CaptureVideo(self.h_cam, ueye.IS_DONT_WAIT)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_CaptureVideo")

        ret = ueye.is_InquireImageMem(self.h_cam, self.pcImageMemory, self.MemID, self.width, self.height,
                                      self.nBitsPerPixel, self.pitch)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_InquireImageMem")

    def stop_video(self):
        ret = ueye.is_StopLiveVideo(self.h_cam, ueye.IS_DONT_WAIT)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_StopLiveVideo")

    def alloc(self):
        ret = ueye.is_AllocImageMem(self.h_cam, self.width, self.height, self.nBitsPerPixel, self.pcImageMemory,
                                    self.MemID)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_AllocImageMem")
        else:
            # Makes the specified image memory the active memory
            ret = ueye.is_SetImageMem(self.h_cam, self.pcImageMemory, self.MemID)
            if ret != ueye.IS_SUCCESS:
                raise uEye_ERROR("is_SetImageMem")

    def un_alloc(self):
        ret = ueye.is_FreeImageMem(self.h_cam, self.pcImageMemory, self.MemID)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_FreeImageMem")
        else:
            self.MemID = ueye.int()
            self.pcImageMemory = ueye.c_mem_p()
            self.pitch = ueye.INT()

    def stop_camera(self):
        ueye.is_ExitCamera(self.h_cam)

    def get_mem_info(self):
        w = ueye.INT()
        h = ueye.INT()
        bit = ueye.INT()
        pit = ueye.INT()
        ret = ueye.is_InquireImageMem(self.h_cam, self.pcImageMemory, self.MemID, w, h, bit, pit)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("get_MemInfo")
        print(w.value, h.value, bit.value, pit.value)

    def get_image(self):
        return ueye.get_data(self.pcImageMemory, self.width, self.height, self.nBitsPerPixel, self.pitch, copy=False)

    def get_aoi(self):
        aoi = ueye.IS_RECT()
        ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_GET_AOI, aoi, ueye.sizeof(aoi))

        return aoi.s32X.value, aoi.s32Y.value, aoi.s32Width.value, aoi.s32Height.value

    def set_aoi(self, x, y, w, h):
        """
        Set the AOI according to the given parameters. The AOI size is adjusted to the closest (smaller) possible size

        :param x: x coordinate (width) of the top left corner of the AOI
        :param y: y coordinate (height) of the top left corner of the AOI
        :param w: width of the AOI
        :param h: height of the AOI
        :return: No return
        """
        x0, y0, w0, h0 = adjust_aoi(x, y, w, h)  # Adjust the size of the AOI

        self.width = ueye.INT(w0)
        self.height = ueye.INT(h0)
        aoi = ueye.IS_RECT()
        aoi.s32X = ueye.INT(x0)
        aoi.s32Y = ueye.INT(y0)
        aoi.s32Width = ueye.INT(w0)
        aoi.s32Height = ueye.INT(h0)

        ret = ueye.is_AOI(self.h_cam, ueye.IS_AOI_IMAGE_SET_AOI, aoi, ueye.sizeof(aoi))
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_AOI")

    def get_colormode(self):
        return ueye.is_SetColorMode(self.h_cam, ueye.IS_GET_COLOR_MODE)

    def set_colormode(self, mode):
        """
        Set the camera color mode to the given color mode.

        :param mode: color mode we want to set
        :return: No return
        """
        ret = ueye.is_SetColorMode(self.h_cam, mode)
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("is_SetColorMode")
        self.nBitsPerPixel = get_bits_per_pixel(mode)
        self.colormode = mode

    def is_colormode(self, mode):
        """
        Test if the colormode is valid.

        Parameters
        ----------
        mode : int (from ueye)
            Mode of color to test.

        Returns
        -------
        bool : True if mode is compatible.
        """
        old_mode = self.get_colormode()
        ret = ueye.is_SetColorMode(self.h_cam, mode)
        self.set_colormode(old_mode)
        if ret != ueye.IS_SUCCESS:
            return False
        else:
            return True

    def get_exposure(self):
        exposure = ueye.double()
        ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE, exposure, ueye.sizeof(exposure))

        return exposure.value

    def get_exposure_range(self):
        min_exposure = ueye.double()
        max_exposure = ueye.double()
        ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN, min_exposure,
                         ueye.sizeof(min_exposure))
        ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX, max_exposure,
                         ueye.sizeof(max_exposure))

        return int(min_exposure.value), int(max_exposure.value)

    def set_exposure_time(self, exposure):
        v = ueye.double(exposure)
        ueye.is_Exposure(self.h_cam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, v, ueye.sizeof(v))

    def get_frame_rate(self):
        fps = ueye.double()
        ueye.is_GetFramesPerSecond(self.h_cam, fps)
        return int(fps)

    def get_frame_time_range(self):
        min_t = ueye.DOUBLE()
        max_t = ueye.DOUBLE()
        step_t = ueye.DOUBLE()
        ueye.is_GetFrameTimeRange(self.h_cam, min_t, max_t, step_t)
        return min_t.value, max_t.value, step_t.value

    def get_frame_rate_range(self):
        min_t, max_t, step_t = self.get_frame_time_range()
        return 1 / max_t, 1 / min_t, 1 / step_t

    def set_frame_rate(self, fps):
        set_fps = ueye.double(fps)
        new_fps = ueye.double()
        ueye.is_SetFrameRate(self.h_cam, set_fps, new_fps)
        return int(new_fps)

    def get_pixel_clock(self):
        pixel_clock = ueye.uint()
        ret = ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_GET, pixel_clock, ueye.sizeof(pixel_clock))
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("get_PixelClock")
            return None
        else:
            return pixel_clock.value

    def set_pixel_clock(self, value):
        pixel_clock = ueye.uint(value)
        ret = ueye.is_PixelClock(self.h_cam, ueye.IS_PIXELCLOCK_CMD_SET, pixel_clock, ueye.sizeof(pixel_clock))
        if ret != ueye.IS_SUCCESS:
            raise uEye_ERROR("set_PixelClock")

    def get_black_level(self):
        blacklevel = ueye.uint()
        ueye.is_Blacklevel(self.h_cam, ueye.IS_BLACKLEVEL_CMD_GET_OFFSET, blacklevel, ueye.sizeof(blacklevel))
        return blacklevel

    def set_black_level(self, value):
        blacklevel = ueye.uint(value)
        ueye.is_Blacklevel(self.h_cam, ueye.IS_BLACKLEVEL_CMD_SET_OFFSET, blacklevel, ueye.sizeof(blacklevel))


# -------------------------------------------------------------------------------------------------------


def get_cam_color_mode(user_color_mode):
    """
    Returns the number of bits per pixel for the given color mode raises exception if color mode is not is
    not in dict

    :param color_mode: color mode for which we want the number of bits per pixel
    :return : number of bits per pixel of the given color mode
    """

    return {
        "MONO8": ueye.IS_CM_MONO8,
        "MONO10": ueye.IS_CM_MONO10,
        "MONO12": ueye.IS_CM_MONO12,

    }[user_color_mode]


def get_bits_per_pixel(color_mode):
    """
    Returns the number of bits per pixel for the given color mode raises exception if color mode is not is
    not in dict

    :param color_mode: color mode for which we want the number of bits per pixel
    :return : number of bits per pixel of the given color mode
    """

    return {
        ueye.IS_CM_SENSOR_RAW8: ueye.INT(8),
        ueye.IS_CM_SENSOR_RAW10: ueye.INT(16),
        ueye.IS_CM_SENSOR_RAW12: ueye.INT(16),
        ueye.IS_CM_SENSOR_RAW16: ueye.INT(16),
        ueye.IS_CM_MONO8: ueye.INT(8),
        ueye.IS_CM_MONO10: ueye.INT(10),
        ueye.IS_CM_MONO12: ueye.INT(12),
        ueye.IS_CM_RGB8_PACKED: ueye.INT(24),
        ueye.IS_CM_BGR8_PACKED: ueye.INT(24),
        ueye.IS_CM_RGBA8_PACKED: ueye.INT(32),
        ueye.IS_CM_BGRA8_PACKED: ueye.INT(32),
        ueye.IS_CM_BGR10_PACKED: ueye.INT(32),
        ueye.IS_CM_RGB10_PACKED: ueye.INT(32),
        ueye.IS_CM_BGRA12_UNPACKED: ueye.INT(64),
        ueye.IS_CM_BGR12_UNPACKED: ueye.INT(48),
        ueye.IS_CM_BGRY8_PACKED: ueye.INT(32),
        ueye.IS_CM_BGR565_PACKED: ueye.INT(16),
        ueye.IS_CM_BGR5_PACKED: ueye.INT(16),
        ueye.IS_CM_UYVY_PACKED: ueye.INT(16),
        ueye.IS_CM_UYVY_MONO_PACKED: ueye.INT(16),
        ueye.IS_CM_UYVY_BAYER_PACKED: ueye.INT(16),
        ueye.IS_CM_CBYCRY_PACKED: ueye.INT(16),
    }[color_mode]


def adjust_aoi(x, y, width, height):
    """
    Adjust the AOI parameters to the closest (smaller) possible size.
    The possibles sizes are defined by:
        - 0 <= x <= 2456 pixels with 4 pixels step
        - 0 <= y <= 2054 pixels with 2 pixels step
        - 256 <= width <= 2456 pixels with 8 pixels step
        - 256 <= height <= 2056 pixels with 2 pixels step

    :param x: x coordinate (width) of the top left corner of the AOI
    :param y: y coordinate (height) of the top left corner of the AOI
    :param width: width of the AOI
    :param height: height of the AOI
    :return: same AOI parameter adjusted to the closest (smaller) possible size
    """
    if x < 0:
        x0 = 0
    elif x > 2456:
        x0 = 2456
    else:
        x0 = x - x % 4

    if y < 0:
        y0 = 0
    elif x > 2054:
        y0 = 2054
    else:
        y0 = y - y % 2

    if width < 256:
        width0 = 256
    elif width > 2456:
        width0 = 2456
    else:
        width0 = width - width % 8

    if height < 256:
        height0 = 256
    elif height > 2054:
        height0 = 2054
    else:
        height0 = height - height % 2

    return x0, y0, width0, height0


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    camera = uEyeCamera(0)
    ser_no, cam_id = camera.get_cam_info()

    print(f'Serial = {ser_no} / ID = {cam_id}')

    camera.set_frame_rate(10)

    camera.set_exposure_time(40)
    camera.set_colormode(get_cam_color_mode("MONO12"))
    max_w = camera.get_sensor_max_width()
    max_h = camera.get_sensor_max_height()
    print(f'M_W = {max_w} / M_H = {max_h}')
    camera.set_aoi(0, 0, max_w, max_h)
    camera.alloc()
    camera.capture_video()
    time.sleep(0.2)
    frame_list = []
    for i in range(10):
        print(i)
        frame = camera.get_image()
        aoi_x, aoi_y, aoi_w, aoi_h = camera.get_aoi()
        if camera.nBitsPerPixel.value > 8:
            # Raw data array for analysis
            camera_raw_frame = frame.view(np.uint16)
            camera_frame = np.reshape(camera_raw_frame, (aoi_h, aoi_w, -1))

            # 8bits array for frame displaying.
            camera_frame_8b = camera_frame / (2 ** (camera.nBitsPerPixel.value - 8))
            camera_array = camera_frame_8b.astype(np.uint8)
        else:
            camera_raw_frame = frame.view(np.uint8)
            camera_array = camera_raw_frame
        frame_list.append(camera_array)
        camera.stop_video()
        camera.un_alloc()
        camera.set_aoi(200, 300, 1000, 400)
        camera.alloc()
        camera.capture_video()
        time.sleep(0.2)

    frame = camera.get_image()
    camera.stop_video()
    camera.un_alloc()
    print(type(frame))
    print(frame.shape)

    for i in range(10):
        plt.imshow(frame_list[i])
        plt.show()

    # Test of capture duration
    camera.set_aoi(0, 0, max_w, max_h)
    time0 = time.time()
    camera.alloc()
    camera.capture_video()
    time.sleep(0.2)
    time1 = time.time()
    frame = camera.get_image()
    time2 = time.time()
    aoi_x, aoi_y, aoi_w, aoi_h = camera.get_aoi()
    time3 = time.time()
    if camera.nBitsPerPixel.value > 8:
        # Raw data array for analysis
        camera_raw_frame = frame.view(np.uint16)
        camera_frame = np.reshape(camera_raw_frame, (aoi_h, aoi_w, -1))

        # 8bits array for frame displaying.
        camera_frame_8b = camera_frame / (2 ** (camera.nBitsPerPixel.value - 8))
        camera_array = camera_frame_8b.astype(np.uint8)
    else:
        camera_raw_frame = frame.view(np.uint8)
        camera_array = camera_raw_frame
    time4 = time.time()
    plt.imshow(camera_array)
    plt.show()

    print(f'starting Time = {int((time1-time0)*1000000)} us')
    print(f'get_image Time = {int((time2-time1)*1000000)} us')
    print(f'get_aoi Time = {int((time3-time2)*1000000)} us')
    print(f'reshape Time = {int((time4-time3)*1000000)} us')

    # Stop Camera
    camera.stop_camera()