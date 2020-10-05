#!/usr/bin/env python3

from smbus2 import SMBus

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
bus = SMBus(0x1e)

b = bus.read_byte_data(0x0F, 0)
print(b)
