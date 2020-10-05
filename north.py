import time
import sys
import arduino_driver_py3 as ardudrv
import compass_drivers as compass

if __name__ == "__main__":
    cx = 4038.0
    cy = -3357.5
    cz = 5237.5
    while True:
        x, y, z = compass.read_compass()
        serial_arduino, data_arduino = ardudrv.init_arduino_line()
        ty = y - cy
        if (ty > 0):
            ardudrv.send_arduino_cmd_motor(serial_arduino, 20, 0)
        elif (ty < 0):
            ardudrv.send_arduino_cmd_motor(serial_arduino, 0, 20)
        else:
            ardudrv.send_arduino_cmd_motor(serial_arduino, 0, 0)
