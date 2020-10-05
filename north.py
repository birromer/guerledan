import time
import sys
import arduino_driver_py3 as ardudrv
import compass_drivers as compass
import numpy as np
from math import pi

def norm(x):
    return (x - pi)/(pi + pi)

def sawtooth(x):
    return (x+pi)%(2*pi)-pi 

if __name__ == "__main__":
    cx = 4038.0
    cy = -3357.5
    cz = 5237.5
    psibar = 0
    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    while True:
        x, y, z = compass.read_compass()
        ty = y - cy
        tx = x - cx
        psi = np.arctan2(ty, tx)
        error = sawtooth(psi - psibar)
        error_norm = norm(error)
        print("error: " + str(error))
        if (error > 0):
            ardudrv.send_arduino_cmd_motor(serial_arduino, error_norm * 50,(1 -
                error_norm) * 50)
        elif (error < 0):
            ardudrv.send_arduino_cmd_motor(serial_arduino, (1 - error_norm) *
                    50, error_norm * 50)
        else:
            ardudrv.send_arduino_cmd_motor(serial_arduino, 0, 0)
        time.sleep(0.25)
