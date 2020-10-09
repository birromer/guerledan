#!/usr/bin/env python3

import drivers.compass_drivers as compdrv
import drivers.arduino_driver_py3 as ardudrv
import drivers.gps_driver_py3 as gpsdrv
import time
import numpy as np
from numpy import pi

def norm(x):
    return (x - pi)/(pi + pi)

def sawtooth(x):
    return (x+pi)%(2*pi)-pi

def g():  # get the readings from the sensors
    x, y, z = compass.read_compass()
    pt = np.array(([x, y, z]))
    pt = opt_pt(pt)
    return pt

def gen_command(readings, psibar, derivate=-10.0):
    pt_x = readings[0]
    pt_y = readings[1]

    psi = np.arctan2(pt_y, pt_x)
    if (derivate != -10.0):
        error = sawtooth(psi - psibar) + sin(psi - derivate)
    else:
        error = sawtooth(psi - psibar)
    n = abs(norm(error))
    def set_range(range_angle, angle):
        if (angle > 0.5 + range_angle):
            return 1
        elif (angle < 0.5 - range_angle):
            return 0
        else:
            return 0.5
    return (set_range(0.0174533, n), n)

def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, power ,time=60):
    if (cmd == 0):
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, rspeed * 1.2)
    elif (cmd == 1):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * 1.2, 0)
    elif (cmd == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * 2, rspeed * 2)

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



if __name__ == "__main__":
    compdrv.init_compass()
    gps = gpsdrv.init_line()
    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    psibar = 0.0
    speeds = [(10,10), (20,20), (40,40), (60,60), (90,90), (120,120), (150,150)]
    measurements = {}  # measurements[speed] = ((cx, cy, cz), (gx, gy, gz)) compass and gps

    # -> alternative where compass stays with divergent value as long as there's a motor working
    # follow the cap before <--------------

    for speed in speeds:
        print("Rspeed:", speed[0], "- Lspeed:", speed[1])
        start_time = time.time()
        speed_mes = np.array([[0], [0], [0], [0], [0], [0]])
        while time.time() - start_time < 10:  # loop for 10 seconds
            # control according to the cap
            x, y, z = compdrv.read_compass()
            pt = np.array(([x, y, z]))
            pt = opt_pt(pt)
            (command, power) = gen_command(pt, psibar, )
            send_command(command, speed[0], speed[1], serial_arduino, data_arduino, power)
            if time.time() - start_time <= 1:
                cx, cy, cz = compdrv.read_compass()
                gps_r = gpsdrv.read_gll(gps)
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
