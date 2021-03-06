import time
import sys
import drivers.arduino_driver_py3 as ardudrv
import drivers.compass_drivers as compass
import numpy as np
from math import pi
import drivers.acc_gyro_driver as acc

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


def gen_command(readings, psibar, derivate=-10.0):
    pt_x = readings[0]
    pt_y = readings[1]

    psi = np.arctan2(pt_y, pt_x)
    if (derivate != -10.0):
        error = sawtooth(psi - psibar) + np.sin(psi - derivate)
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
    return (set_range(0.0174533, n), n, psi)


def send_prop_command(side, sum_speed, power, seria_artudino):
    print("power:", power)
    if (side == 0):  # it is too much to the right
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, sum_speed * 1.2)
    elif (side == 1):  # it is too much to the left
        ardudrv.send_arduino_cmd_motor(serial_arduino, sum_speed * 1.2, 0)
    elif (side == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, sum_speed * 2, sum_speed * 2)


def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, power ,time=60):
    if (cmd == 0):
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, rspeed)
    elif (cmd == 1):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed, 0)
    elif (cmd == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * 1.2, rspeed * 1.2)

if __name__ == "__main__": #thresh = 12 000 cmdl = 50 cmdr = 50
    cmdl = 20
    cmdr = 20
    psibar = 0  # ticks/s
    thresh_bump = 1500

    try:
        thresh_bump = int(sys.argv[1])
    except:
        pass
    try:
        cmdl = int(sys.argv[2])
        cmdr = cmdl
    except:
        pass
    try:
        cmdr = int(sys.argv[3])
    except:
        pass
    try:
        psibar = int(sys.argv[4]) * 0.0174533
    except:
        pass


    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    bump_thresh = sys.argv[1]
    acc.init_acc_gyro()
    compass.init_compass()

    start_time = time.time()
    state = "OFF"
    event = "None"
    old_psi = -10.0
    #psibar = desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
    i = 0
    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))
        pt = opt_pt(pt)
        if (state == "OFF"):
            psibar = pi/4
            old_psi = -10.0
            event = "None"
            state = "WAIT"
            print("WAIT STATE")
        elif (state == "ON"):
            if (event == "Forward"):
                if (acc.is_bump(bump_thresh)):
                    ardudrv.send_arduino_cmd_motor(serial_arduino, 0, 0)
                    time.sleep(4)
                    i += 1
                    print("-------> bump " + str(i))
                    psibar += pi/2
                    psibar %= 2*pi
                    state = "WAIT"
                    print("WAIT STATE, go to:", psibar*57.2958)
        elif (state == "WAIT"): #speed should be decreased on wait
            pt_x = pt[0]
            pt_y = pt[1]
            psi = np.arctan2(pt_y, pt_x)
            if (abs(sawtooth(psi - psibar)) < 0.05):
                state = "ON"
                event = "Forward"
                print("ON STATE")

        (command, power, old_psi) = gen_command(pt, psibar, old_psi )
        send_command(command, cmdr, cmdl, serial_arduino, data_arduino, power)
