import time
import drivers.arduino_driver_py3 as ardudrv
import drivers.compass_drivers as compass
import numpy as np
from math import pi

def norm(x):
    return (x - pi)/(pi + pi)

def sawtooth(x):
    return (x+pi)%(2*pi)-pi

def opt2(pt, x1, xm1, x2, x3):
    A = np.zeros((3,3))
    xv = np.array([x1,x2,x3])
    beta = 0.0000047

    b = -(x1 + xm1)/2

    A[:,0] = (x1 + b)/beta
    A[:,1] = (x2 + b)/beta
    A[:,2] = (x3 + b)/beta

    opt_pt = np.matmul(np.linalg.inv(A), (pt + b))

    return opt_pt

def sending_command(serial_arduino, data_arduino, lspeed, rspeed, time=60):
    x1 = np.array([900, -3950, 5540])
    xm1 = np.array([7050, -2950, 5400])
    x2 = np.array([4410, -6400, 5450])
    x3 = np.array([3950, -3450, 2300])

    psibar = 0

    while (True):
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))

        opt_pt = opt2(pt, x1, xm1, x2, x3)
        #print("x:", opt_pt[0], ", y:", opt_pt[1], ", z:", opt_pt[2])

        psi = np.arctan2(opt_pt[1], opt_pt[0])
        error = sawtooth(psi - psibar)
        n = abs(norm(error))

        #print("error: " + str(error))

        def bla(x):
            if x > 0.5:
                return 1
            else:
                return 0

        ardudrv.send_arduino_cmd_motor(serial_arduino, bla(n) * lspeed, (1 -
            bla(n)) * rspeed)

        #time.sleep(0.25)


if __name__ == "__main__":
    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    sending_command(serial_arduino, data_arduino, 60, 60)
