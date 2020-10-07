import time
import drivers.arduino_driver_py3 as ardudrv
import drivers.compass_drivers as compass
import numpy as np
from math import pi

def convert_to_degree(x):
    return ((x*360 -180))

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
    def set_range(range_angle, angle):
        if (angle > 0.5 + range_angle):
            return 1
        elif (angle < 0.5 - range_angle):
            return 0
        else:
            return 0.5
    return set_range(0.0523599, n)


def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, time=60):
    if (cmd == 0):
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, rspeed)
    elif (cmd == 1):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed, 0)
    elif (cmd == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed, rspeed)

if __name__ == "__main__":
    serial_arduino, data_arduino = ardudrv.init_arduino_line()


    start_time = time.time()
    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))
        pt = opt_pt(pt)
        get_time = time.time()
        time_cur = get_time - start_time
        print("time: ", time_cur)
        if (time_cur < 5):
                psibar = -pi/2  #desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
        elif (time_cur < 10):
                psibar = pi  #desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
        elif (time_cur < 15):
                psibar = pi/2  #desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
        elif (time_cur < 20):
                psibar = 0  #desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
        else:
            send_command(command, 0, 0, serial_arduino, data_arduino)
            break
        command = gen_command(pt, psibar)
        send_command(command, 40, 30, serial_arduino, data_arduino)
