import time
import drivers.arduino_driver_py3 as ardudrv
import drivers.compass_drivers as compass
import numpy as np
from math import pi

def norm(x):
    return (x - pi)/(pi + pi)

def sawtooth(x):
    return (x+pi)%(2*pi)-pi

def opt_pt(pt):
    x1 = np.array([900, -3950, 5540])
    xm1 = np.array([7050, -2950, 5400])
    x2 = np.array([4410, -6400, 5450])
    x3 = np.array([3950, -3450, 2300])

    A = np.zeros((3,3))
    xv = np.array([x1,x2,x3])
    beta = 0.0000047

    b = -(x1 + xm1)/2

    A[:,0] = (x1 + b)/beta
    A[:,1] = (x2 + b)/beta
    A[:,2] = (x3 + b)/beta

    pt = np.matmul(np.linalg.inv(A), (pt + b))

    return pt

def g():  # get the readings from the sensors
    x, y, z = compass.read_compass()
    pt = np.array(([x, y, z]))
    pt = opt_pt(pt)
    return pt


def gen_command(readings, psibar):
    pt_x = readings[0]
    pt_y = readings[1]

    psi = np.arctan2(pt_y, pt_x)
    error = sawtooth(psi - psibar)

    n = abs(norm(error))
    print(n)
    on = lambda x: 1 if x > 0.5 else 0

    return on(n)


def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, time=60):
    ardudrv.send_arduino_cmd_motor(serial_arduino, cmd * lspeed, (1 - cmd) * rspeed)
    #time.sleep(0.25)


if __name__ == "__main__":
    serial_arduino, data_arduino = ardudrv.init_arduino_line()

    psibar = 0  # desired heading (0 = north)

    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))
        print(pt)
        pt = opt_pt(pt)
        command = gen_command(pt, psibar)
        send_command(command, 60, 60, serial_arduino, data_arduino)
