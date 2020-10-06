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

def opt(pt, p):
    p1, p2, p3 = p[0], p[1], p[2]
    p4, p5, p6 = p[3], p[4], p[5]
    x, y, z = pt[0], pt[1], pt[2]

    fp_1 = np.array([
        [p4, 0, 0],
        [0, p5, 0],
        [0, 0, p6]
    ], dtype=float)

    fp_2 = np.array([
        x - p1,
        y - p2,
        z - p3
    ], dtype=float)

    return fp_1 @ fp_2

if __name__ == "__main__":
    cx, cy, cz = 4038.0, -3357.5, 5237.5
    lx, ly, lz = 5958.0, 5697.0, 5867.0
    p = np.array([
        cx,cy,cy,lx,ly,lz
    ])

    psibar = 0
    serial_arduino, data_arduino = ardudrv.init_arduino_line()

    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))

        bla = opt(pt, p)
        print("tem:", bla)

        ty = y - cy
        tx = x - cx

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
