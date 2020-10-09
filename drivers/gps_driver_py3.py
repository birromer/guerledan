import serial
import os
import time

def init_line():
    ser = serial.Serial('/dev/ttyS0',timeout=1.0)
    time.sleep(1.0)
    print(ser)
    return ser

def read_gll(ser,nmax=20):
    val=[0.,'N',0.,'W',0.]
    for i in range(nmax):
        v=ser.readline().decode("utf-8")
        if str(v[0:6]) == "$GPGLL":
            vv = v.split(",")
            try:
                val[0] = float(vv[1])
                val[1] = vv[2]
            except:
                val[0] = 0.0
                val[1] = "N"

            try:
                val[2] = float(vv[3])
                val[3] = vv[4]
            except:
                val[2] = 0.0
                val[3] = "W"

            val[4] = float(vv[5])
            break
    return val
   

def close(ser):
    ser.close()
