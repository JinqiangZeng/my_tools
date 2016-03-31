#!/usr/bin/python
import serialPortDetect
import serial
from time import sleep, time
import sys
import json
import matplotlib.pyplot as plt
import os

"""
Test cases for LSM9DS0, the 9 axies accelerometer/gyrocscope/magnetometer sensor
"""

serialfd = serial.Serial(serialPortDetect.serial_ports()[0], 115200, timeout=0.5)

TLEN = 1000
#plot handler
plotArrays = {}
#time axia[second]
tArray = [i * 0.01 for i in range(TLEN)]
xArray = []
yArray = []
zArray = []
plotDir = 'output/plot'

if not os.path.exists(plotDir):
    os.makedirs(plotDir)

def arrayInit():
    global xArray, yArray, zArray
    del xArray[:]
    del yArray[:]
    del zArray[:]

def addToArray(s):
    jstr = json.loads(s)
    xArray.append(jstr['x'])
    yArray.append(jstr['y'])
    zArray.append(jstr['z'])

def plotOnearray(pa, duration, figname):
    vmax = max(pa)
    vmin = min(pa)

    if vmax < 0:
        vmax *= 0.9
    else:
        vmax *= 1.1

    if vmin < 0:
        vmin *= 1.1
    else:
        vmin *= 0.9

    plt.axis([0,duration,vmin, vmax ])
    plt.plot(tArray, pa)
    plt.savefig(figname)
    plt.cla()


def plotArrays(s_type, duration):
    plotOnearray(xArray, duration, plotDir + '/' + s_type + '_x.png')
    plotOnearray(yArray, duration, plotDir + '/' + s_type + '_y.png')
    plotOnearray(zArray, duration, plotDir + '/' + s_type + '_z.png')

def sensorTest(cmd):
    global tArray
    start = time()
    arrayInit()
    for i in range(0,TLEN):
        serialfd.write(cmd + "\r\n")
        serialfd.write("\r\n")
        sleep(0.01)
        str = serialfd.readline()
        print(str.strip('\r\n'))
        addToArray(str)
    duration = time() - start
    tArray = [i*duration/TLEN for i in range(TLEN)]
    plotArrays(cmd, duration)
    print("---------{} seconds---------".format(time() - start))

def stest():
    for i in range(0,TLEN):
        serialfd.write("sensors_get\r\n")
        serialfd.write("\r\n")
        sleep(0.01)
        str = serialfd.readline()
        print(str.strip('\r\n'))

def gyro_cal():
    serialfd.write("gyro_cal\r\n")
    print(serialfd.readline())

if __name__ == '__main__':
    while True:
        cmd = raw_input("leia> ")
        if cmd == "angle":
            sensorTest('angle')
        elif cmd == "gyro":
            sensorTest('gyro_get')
        elif cmd == "gyro_cal":
            gyro_cal()
        elif cmd == "acc":
            sensorTest('accel_get')
        elif cmd == "exit":
            sys.exit()
        elif cmd == "mag":
            sensorTest('mag_get')
        elif cmd == "sensors":
            stest()

