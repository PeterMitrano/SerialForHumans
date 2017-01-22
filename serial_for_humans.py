#!/usr/bin/python3.5

import sys
import serial
from serial_for_humans import App


if __name__ == '__main__':
    if '--debug' in sys.argv:
        import time
        time.sleep(10)

    if len(sys.argv) < 3:
        print("Usage: python main.py port_path baudrate")
        print()
        print("EX: python main.py /dev/ttyUSB0 9600")
    else:
        port = sys.argv[1]
        baudrate = int(sys.argv[2])

        app = App()
        serial = serial.Serial(port, baudrate, timeout=0)
        app.run(serial)
