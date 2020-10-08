#!/usr/bin/env python3

from smbus import SMBus
import time

# device address in the bus
DEV_ADDR = 0x6b

# registers
WHO_AM_I   = 0x0F

#  fifo configuration
CTRL_REG1  = 0x06
CTRL_REG2  = 0x07
CTRL_REG3  = 0x08
CTRL_REG4  = 0x09
CTRL_REG5  = 0x0A

ORIENT_CFG_G = 0X0b

#  acc and gyro control
CTRL1_XL  = 0x10
CTRL2_G   = 0x11
CTRL3_C   = 0x11
CTRL4_C   = 0x11
CTRL5_C   = 0x11
CTRL6_C   = 0x11
CTRL7_G   = 0x11
CTRL8_XL  = 0x11
CTRL9_XL  = 0x11
CTRL10_C  = 0x11

STATUS_REG = 0x1E

#  gyro output data
OUTX_L_G = 0x22
OUTX_H_G = 0x23
OUTY_L_G = 0x24
OUTY_H_G = 0x25
OUTZ_L_G = 0x26
OUTZ_H_G = 0x27

#  acc ooutput data
OUTX_L_XL = 0x28
OUTX_H_XL = 0x29
OUTY_L_XL = 0x2A
OUTY_H_XL = 0x2B
OUTZ_L_XL = 0x2C
OUTZ_H_XL = 0x2D

#  fifo status
FIFO_STATUS_1 = 0x3A
FIFO_STATUS_2 = 0x3B
FIFO_STATUS_3 = 0x3C
FIFO_STATUS_4 = 0x3D

#  fifo output data
FIFO_DATA_OUT_L = 0x3E
FIFO_DATA_OUT_H = 0x3F

#  interruptions control
INT1_CTRL = 0x0D
INT2_CTRL = 0x0E


# access to special functions configuration
FUNC_CFG_ACCESS = 0x01

#  access to interruption status
FUNC_SRC = 0x53

#  significant motion threshold configuration
SM_THS = 0x13

## connecting to the bus ##
bus = SMBus(1)

# who am i information
def who_am_i():
    b = bus.read_byte_data(DEV_ADDR, WHO_AM_I)
    print("WHO AM I data:", hex(b))


# configuring the ctrl regs
def init_acc_gyro():
    data1  = 0b10100111 
    data2  = 0b10100000
    data3  = 0b00000000
    data4  = 0b10000000
    data5  = 0b01100100
    data6  = 0b00100000
    data7  = 0b00000000
    data8  = 0b10100101  # low pass enable for acc, !!!check that later!!!
    data9  = 0b00111000  # enable gyro axis
    data10 = 0b00111101  # enable acc axis and special functions

    data_int1 = 0b01000000  # enable significant motion interruption

    bus.write_byte_data(DEV_ADDR, CTRL1_XL, data1)
    bus.write_byte_data(DEV_ADDR, CTRL2_G,  data2)
    bus.write_byte_data(DEV_ADDR, CTRL3_C,  data3)
    bus.write_byte_data(DEV_ADDR, CTRL4_C,  data4)
    bus.write_byte_data(DEV_ADDR, CTRL5_C,  data5)
    bus.write_byte_data(DEV_ADDR, CTRL6_C,  data6)
    bus.write_byte_data(DEV_ADDR, CTRL7_G,  data7)
    bus.write_byte_data(DEV_ADDR, CTRL8_XL, data8)
    bus.write_byte_data(DEV_ADDR, CTRL9_XL, data9)
    bus.write_byte_data(DEV_ADDR, CTRL10_C, data10)

    bus.write_byte_data(DEV_ADDR, INT1_CTRL, data_int1)


def read_gyro():
    x_h = bus.read_byte_data(DEV_ADDR, OUTX_H_G)
    x_l = bus.read_byte_data(DEV_ADDR, OUTX_L_G)
    x = x_h*2**8 + x_l
    if (x > 32767):
        x = x - 65536

    y_h = bus.read_byte_data(DEV_ADDR, OUTY_H_G)
    y_l = bus.read_byte_data(DEV_ADDR, OUTY_L_G)
    y = y_h*2**8 + y_l
    if (y > 32767):
        y = y - 65536

    z_h = bus.read_byte_data(DEV_ADDR, OUTZ_H_G)
    z_l = bus.read_byte_data(DEV_ADDR, OUTZ_L_G)
    z = z_h*2**8 + z_l
    if (z > 32767):
        z = z - 65536

    return x, y, z


def read_acc():
    x_h = bus.read_byte_data(DEV_ADDR, OUTX_H_XL)
    x_l = bus.read_byte_data(DEV_ADDR, OUTX_L_XL)
    x = x_h*2**8 + x_l
    if (x > 32767):
        x = x - 65536

    y_h = bus.read_byte_data(DEV_ADDR, OUTY_H_XL)
    y_l = bus.read_byte_data(DEV_ADDR, OUTY_L_XL)
    y = y_h*2**8 + y_l
    if (y > 32767):
        y = y - 65536

    z_h = bus.read_byte_data(DEV_ADDR, OUTZ_H_XL)
    z_l = bus.read_byte_data(DEV_ADDR, OUTZ_L_XL)
    z = z_h*2**8 + z_l
    if (z > 32767):
        z = z - 65536

    return x, y, z

def is_significant_motion():
    v = bus.read_byte_data(DEV_ADDR, FUNC_SRC)
    desired = 0b00100000  # position of the significant motion
    st = v & desired

    if st != 0:
        return True
    else:
        return False


def is_bump():
    bump = lambda x: True if abs(ax) > 1500 else False
#    prev_bump = # put the timestamp to test if bump is recent
    return bump(ax) or bump(ay)

ax, ay, az = 0, 0, 0


if __name__ == "__main__":
    prev_bump_t = 0

    who_am_i()

    init_acc_gyro()
    gyro_f = open("../data/gyro.txt", "w")
    acc_f = open("../data/acc.txt", "w")

    prev_ax = 0
    prev_ay = 0
    prev_az = 0

    while True:
        gx, gy, gz = read_gyro()
        ax, ay, az = read_acc()

        gyro_f.write("%d %d %d\n"%(gx, gy, gz))
        acc_f.write("%d %d %d\n"%(ax, ay, az))

        if is_significant_motion():
            print("significant motion")

        if is_bump():
            print("BUMP!")
            print()

#        print("dif x:", ax - prev_ax)
#        print("dif y:", ay - prev_ay)
#        print("dif z:", az - prev_az)

#        print("Gyro -> X:", gx, "Y:", gy, "Z:", gz)
#        print("Acc  -> X:", ax, "Y:", ay, "Z:", az)
