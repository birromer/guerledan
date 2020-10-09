#!/usr/bin/env python3

import drivers.compass_drivers as compdrv
import drivers.arduino_driver_py3 as ardudrv
import drivers.gps_driver_py3 as gpsdrv
import time
import numpy as np


if __name__ == "__main__":
    compdrv.init_compass()
    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    gps = gpsdrv.init_line()

    speeds = [(0,0), (10,10), (20,20), (40,40), (60,60), (90,90), (120,120), (150,150)]
    measurements = {}  # measurements[speed] = ((cx, cy, cz), (gx, gy, gz)) compass and gps

    # -> alternative where compass stays with divergent value as long as there's a motor working
    # get compass and gps measurements
    cx, cy, cz = compdrv.read_compass()
    gps_r = gpsdrv.read_gll(gps)
    measurements[(0,0)] = ((cx, cy, cz), (gps_r[0], gps_r[2], gps_r[4]))

    for speed in speeds:
        start_time = time.time()
        speed_mes = np.array([[0], [0], [0], [0], [0], [0]])
        while time.time() - start_time < 10:  # loop for 10 seconds
            ardudrv.send_arduino_cmd_motor(serial_arduino, 34, 29)  # accelerates to speed
            if time.time() - start_time <= 1:
                cx, cy, cz = compdrv.read_compass()
                gps_r = gpsdrv.read_gll(ser)
                mes = np.array([[cx], [cy], [cz], [gps_r[0]], [gps_r[2]], [gps_r[4]]])
                speed_mes = np.hstack((speed_mes, mes))
        # get mean and deviation of of compass measurements
        measurements[speed] = ((speed_mes[0,:].mean(), speed_mes[1,:].mean(), speed_mes[2,:].mean()), (speed_mes[3,:].mean(), speed_mes[4,:].mean(), speed_mes[5,:].mean()))
    # get angle error
    print(measurements)


    # -> alternative where compass converges after time to the correct direction
    # for speed in speeds
    #  start time
    #  loop while hasn't converged
    #    accelerate
    #    measure angle diff
    #  end time
