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
    return (set_range(0.0349066, n), n)


def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, power ,time=60):
    if (cmd == 0):
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, rspeed * ((0.5 -
            power) + 1.5))
    elif (cmd == 1):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * (1.5 + power), 0)
    elif (cmd == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * 1.8, rspeed *
                1.8)

if __name__ == "__main__":
    serial_arduino, data_arduino = ardudrv.init_arduino_line()

    compass.init_compass()

    start_time = time.time()
    state = "OFF"
    event = "North"
    psibar = 0
    #psibar = desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))
        pt = opt_pt(pt)
        get_time = time.time()
        time_cur = get_time - start_time
        print("state: " + state + ", event: " + event)
        if (state == "OFF"):
            start_time = time.time()
            psibar = 0
            event = "North"
            state = "ON"
        elif (state == "ON"):
            if (event == "North"):
                if (time_cur < 10):
                    psibar = 0
                else:
                    psibar = -pi/2 + 0.2
                    state = "WAIT"
                    event = "West"
            elif (event == "West"):
                if (time_cur < 20):
                    psibar = -pi/2 + 0.2
                else:
                    psibar = pi + 0.1
                    state = "WAIT"
                    event = "South"
            elif (event == "East"):
                if (time_cur < 20):
                    psibar = pi/2
                else:
                    psibar = 0
                    state = "WAIT"
                    event = "North"
            elif (event == "South"):
                if (time_cur < 10):
                    psibar = pi + 0.1
                else:
                    psibar = pi/2
                    state = "WAIT"
                    event = "East"
        elif (state == "WAIT"): #speed should be decreased on wait
            pt_x = pt[0]
            pt_y = pt[1]
            psi = np.arctan2(pt_y, pt_x)
            if (sawtooth(psi - psibar) < 0.2):
                state = "ON"
                start_time = time.time()

        (command, power) = gen_command(pt, psibar)
        send_command(command, 64, 59, serial_arduino, data_arduino, power)
