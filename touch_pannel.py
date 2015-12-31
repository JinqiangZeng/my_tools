#!/usr/bin/python
import sys
import glob
import serial
from time import sleep
from time import time

"""
This script is used for touch panel test
"""

def serial_ports():
    """ List serial port names
        :raises EnvironmentError:
            On unsupported or unknow platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        #this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.usb*')
    else:
        raise EnvironmentError('unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print result
    return result

def serial_open(port):
    s = serial.Serial(port=port,
                      baudrate=2000000)
    s.open()
    print s.isOpen()

def tp_read():
    ports = serial_ports()
    print ports
    if ports:
        print(ports[0])
        s = serial.Serial(port=ports[0],
                          baudrate = 2000000)
        s.write("ptouch_reset\r\n")
        print(s.readline())
        while 1:
            s.write("i2c_read 0x40 0x07 8\r\n")
            print(s.readline())
            sleep(0.3)
            print(time())
        while 1:
            s.write("ptouch_get\r\n")
            print(s.readline())
            sleep(0.1)
            print(time())
            
def do_cmd_without_par(cmd):
    ports = serial_ports()
    if ports:
        s = serial.Serial(port=ports[0], baudrate = 2000000)
        for i in range(100):
            s.write('{}\r\n'.format(cmd))
            print(s.readline())
            sleep(0.1)
            
def finger():
    ports = serial_ports()
    if ports:
        s = serial.Serial(port=ports[0], baudrate = 2000000)
        for i in range(100):
            s.write('fingers_get 4\r\n')
            print(s.readline())
            sleep(0.1)

def i2c():
    ports = serial_ports()
    if ports:
        s = serial.Serial(port=ports[0], baudrate = 2000000)
        for i in range(4):
            s.write('i2c_read 0x3a {} 1\r\n'.format(0x1F))
            print(s.readline())
            print(s.readline())
            s.write('i2c_write 0x3a {} 0x40\r\n'.format(0x1F))
            print(s.readline())
            print(s.readline())
            s.write('i2c_read 0x3a {} 1\r\n'.format(0x05))
            print(s.readline())
            print(s.readline())
            s.write('i2c_read 0x3a {} 1\r\n'.format(0x06))
            print(s.readline())
            print(s.readline())
            sleep(0.1)

def sensor():
    ports = serial_ports()
    if ports:
        s = serial.Serial(port=ports[0], baudrate = 2000000)
        for i in range(100):
            s.write('temp_get\r\n')
            print(s.readline())
            s.write('accel_get\r\n')
            print(s.readline())
            s.write('mag_get\r\n')
            print(s.readline())
            s.write('gyro_get\r\n')
            print(s.readline())
            s.write('sensors_get\r\n')
            print(s.readline())
            sleep(0.1)

if __name__ == '__main__':
    while 1:
        cmd = raw_input("leia> ")
        if cmd == 'mf':
            do_cmd_without_par("ptouch_mget")
        elif cmd == 'accel':
            do_cmd_without_par("accel_get")
        elif cmd == 'finger':
            finger()
        elif cmd == 'i2c':
            i2c()
        elif cmd == 'sensor':
            sensor()
        elif cmd == 'ac':
            do_cmd_without_par("accel_get")
        elif cmd == 'mag':
            do_cmd_without_par("mag_get")
        elif cmd == 'tp':
            do_cmd_without_par("temp_get")
        elif cmd == 'gy':
            do_cmd_without_par("gyro_get")
        elif cmd == 'ss':
            do_cmd_without_par("sensors_get")
        else:
            print('unknow command')
