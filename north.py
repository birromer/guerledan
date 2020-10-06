import time
import arduino_driver_py3 as ardudrv
import compass_drivers as compass
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

if __name__ == "__main__":
#    cx, cy, cz = 4038.0, -3357.5, 5237.5
#    lx, ly, lz = 5958.0, 5697.0, 5867.0
#    p = np.array([
#        cx,cy,cy,lx,ly,lz
#    ])

    x1 = np.array([900, -3950, 5540])
    xm1 = np.array([7050, -2950, 5400])
    x2 = np.array([4410, -6400, 5450])
    x3 = np.array([3950, -3450, 2300])

    psibar = 0

    serial_arduino, data_arduino = ardudrv.init_arduino_line()

    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))

        opt_pt = opt2(pt, x1, xm1, x2, x3)
        print("x:", opt_pt[0], ", y:", opt_pt[1], ", z:", opt_pt[2])

#        ty = y - cy
#        tx = x - cx

        psi = np.arctan2(opt_pt[1], opt_pt[0])
        error = sawtooth(psi - psibar)
        n = abs(norm(error))

        print("error: " + str(error))

        def bla(x):
            if x > 0.5:
                return 1
            else:
                return 0

        sp_m = 60

        ardudrv.send_arduino_cmd_motor(serial_arduino, bla(n) * sp_m, (1 - bla(n)) * sp_m)

        time.sleep(0.25)
