import serial
import sys
import glob

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
        ports = glob.glob('/dev/cu.usb*')
    else:
        raise EnvironmentError('unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port, 115200, timeout=1)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
