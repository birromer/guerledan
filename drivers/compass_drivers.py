#!/usr/bin/env python3

from smbus import SMBus

# device address in the bus
DEV_ADDR = 0x1e

# registers
WHO_AM_I   = 0x0F

CTRL_REG1  = 0x20
CTRL_REG2  = 0x21
CTRL_REG3  = 0x22
CTRL_REG4  = 0x23
CTRL_REG5  = 0x24

STATUS_REG = 0x27

OUT_X_L    = 0x28
OUT_X_H    = 0x29
OUT_Y_L    = 0x2A
OUT_Y_H    = 0x2B
OUT_Z_L    = 0x2C
OUT_Z_H    = 0x2D

TEMP_OUT_L = 0x2E
TEMP_OUT_H = 0x2F

INT_CFG    = 0X30
INT_SRC    = 0X31
INT_THS_L  = 0x32
INT_THS_H  = 0x33


# connecting to the bus
bus = SMBus(1)


# who am i information
def who_am_i():
    b = bus.read_byte_data(DEV_ADDR, WHO_AM_I)
    print("WHO AM I data:", hex(b))


# configuring the ctrl regs
def init_compass():
    data1 = 0b10111100
    data2 = 0b00000000
    data3 = 0b00000000
    data4 = 0b00000100
    data5 = 0b01000000
    bus.write_byte_data(DEV_ADDR, CTRL_REG1, data1)
    bus.write_byte_data(DEV_ADDR, CTRL_REG2, data2)
    bus.write_byte_data(DEV_ADDR, CTRL_REG3, data3)
    bus.write_byte_data(DEV_ADDR, CTRL_REG4, data4)
    bus.write_byte_data(DEV_ADDR, CTRL_REG5, data5)


def read_compass():
    x_h = bus.read_byte_data(DEV_ADDR, OUT_X_H)
    x_l = bus.read_byte_data(DEV_ADDR, OUT_X_L)
    x = x_h*2**8 + x_l
    if (x > 32767):
        x = x - 65536

#    x = bus.read_i2c_block_data(DEV_ADDR, OUT_X_H, 2)
#    print "X axis:", (x[0]*2**8 + x[1])

    y_h = bus.read_byte_data(DEV_ADDR, OUT_Y_H)
    y_l = bus.read_byte_data(DEV_ADDR, OUT_Y_L)
    y = y_h*2**8 + y_l
    if (y > 32767):
        y = y - 65536

    z_h = bus.read_byte_data(DEV_ADDR, OUT_Z_H)
    z_l = bus.read_byte_data(DEV_ADDR, OUT_Z_L)
    z = z_h*2**8 + z_l
    if (z > 32767):
        z = z - 65536

    return x, y, z


if __name__ == "__main__":
    who_am_i()

    init_compass()

    with open("pts.txt", "w") as f:
        while True:
            x, y, z = read_compass()
            f.write("%d %d %d\n"%(x, y, z))
            print("X:", x, "Y:", y, "Z:", z)
