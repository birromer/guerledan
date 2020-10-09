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
    return (set_range(0.0174533, n), n)


def send_command(cmd, lspeed, rspeed, serial_arduino, data_arduino, power ,time=60):
    if (cmd == 0):
        ardudrv.send_arduino_cmd_motor(serial_arduino, 0, rspeed * ((0.5 -
            power) + 1))
    elif (cmd == 1):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * (1 + power), 0)
    elif (cmd == 0.5):
        ardudrv.send_arduino_cmd_motor(serial_arduino, lspeed * 2.5, rspeed * 2.5)

if __name__ == "__main__":
    cmdl = 20
    cmdr = 20
    spd = 200  # ticks/s
    thresh_bump = 1500

    try:
        thresh_bump = int(sys.argv[1])
    except:
        pass
    try:
        cmdl = int(sys.argv[3])
        cmdr = cmdl
    except:
        pass
    try:
        cmdr = int(sys.argv[4])
    except:
        pass
    try:
        spd = int(sys.argv[2])
    except:
        pass


    serial_arduino, data_arduino = ardudrv.init_arduino_line()
    bump_thresh = sys.argv[1]

    compass.init_compass()

    start_time = time.time()
    state = "OFF"
    event = "None"
    psibar = 0.0
    #psibar = desired heading (0 = north) (pi/2 = east) (pi = south) (-pi/2 = west)
    i = 0
    while True:
        x, y, z = compass.read_compass()
        pt = np.array(([x, y, z]))
        pt = opt_pt(pt)
        if (state == "OFF"):
            psibar = 0.0
            event = "None"
            state = "WAIT"
            print("WAIT STATE")
        elif (state == "ON"):
            if (event == "Forward"):
                if (acc.is_bump(bump_thresh)):
                    i += 1
                    print("-------> bump " + str(i))
                    psibar += pi/3
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

        (command, power) = gen_command(pt, psibar)
        send_command(command, cmdr, cmdl, serial_arduino, data_arduino, power)
