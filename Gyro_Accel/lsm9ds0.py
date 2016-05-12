#!/usr/local/bin/python
import serialPortDetect
import serial
from time import sleep, time
import sys
import json
import matplotlib.pyplot as plt
import os
from timeStatistics import time_cal
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.tri as mtri

"""
Test cases for LSM9DS0, the 9 axies accelerometer/gyroscope/magnetometer sensor
"""

serialfd = serial.Serial(serialPortDetect.serial_ports()[0], 4000000, timeout=2.5)

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

def axisRange(array):
    vmax = max(array)
    vmin = min(array)

    if vmax < 0:
        vmax *= 0.9
    else:
        vmax *= 1.1

    if vmin < 0:
        vmin *= 1.1
    else:
        vmin *= 0.9
    return (vmax, vmin)


def plotOnearray(pa, duration, figname):
    vmax, vmin = axisRange(pa)

    plt.axis([0,duration,vmin, vmax ])
    plt.plot(tArray, pa)
    plt.savefig(figname)
    plt.cla()

def plotTwoArrays(px, py, figname):
    vmax, vmin = axisRange(py)
    hmax, hmin = axisRange(px)

    ax = plt.figure().add_subplot(111)
    plt.axis([hmin, hmax, vmin, vmax])
    plt.grid(True)
    ax.plot(px, py)
    plt.savefig(plotDir + '/' + figname)
    plt.cla()
    plt.close()

"""plot 3d magneto"""
def plot3d(px, py, pz, figname):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.grid(True)
    ax.plot(px, py, pz, label='mag stero')
    ax.legend()
    plt.savefig(plotDir + '/' + figname)
    plt.cla()
    plt.grid(True)
    ax.scatter(px, py, pz, zdir='z', label='mag stero')
    ax.legend()
    plt.savefig(plotDir + '/' + "s"+ figname)
    plt.cla()
    plt.close()

def plotColor3d(x, y, z, figname):
    triang = mtri.Triangulation(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(triang,z, cmap=cm.coolwarm)
    plt.show()
    plt.cla()


def plotArrays(s_type, duration):
    plotOnearray(xArray, duration, plotDir + '/' + s_type + '_x.png')
    plotOnearray(yArray, duration, plotDir + '/' + s_type + '_y.png')
    plotOnearray(zArray, duration, plotDir + '/' + s_type + '_z.png')

@time_cal
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
    if cmd == 'accel_get':
        deltaz = []
        deltaz.append(0)
        deltaz.extend([abs(zArray[i+1]-zArray[i])  for i in range(0, TLEN-1) ])
        plotOnearray(deltaz, duration, plotDir + '/' + '_deltaz.png')

@time_cal
def stest(cmd):
    for i in range(0,TLEN):
        serialfd.write(cmd + "\r\n")
        serialfd.write("\r\n")
        sleep(0.01)
        str = serialfd.readline()
        print(str.strip('\r\n'))

@time_cal
def gyro_cal():
    serialfd.write("gyro_cal\r\n")
    print(serialfd.readline().strip("\r\n"))

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
        elif cmd == "finger":
            stest('fingers_get 2')
        elif cmd == "exit":
            serialfd.close()
            sys.exit()
        elif cmd == "mag":
            sensorTest('mag_get')
            plotTwoArrays(xArray, yArray, "mag_xy.png")
            print("center point max_min is ({}, {}, {})".format(sum(axisRange(xArray))/2.0, sum(axisRange(yArray))/2.0, sum(axisRange(zArray))/2.0))
            print("center point average is ({}, {}, {})".format(sum(xArray)/len(xArray), sum(yArray)/len(yArray), sum(zArray)/len(zArray)))
            print("max point is ({}, {}, {})".format(max(xArray), max(yArray), max(zArray)))
            print("min point is ({}, {}, {})".format(min(xArray), min(yArray), min(zArray)))
            print("radius point is ({}, {}, {})".format((max(xArray) - min(xArray))/2, (max(yArray) - min(yArray))/2, (max(zArray) - min(zArray))/2))
            plot3d(xArray, yArray, zArray, "mag_xyz.png")
            # plotColor3d(xArray, yArray, zArray, "mag_xyz.png")
        elif cmd == "mag_cal":
            serialfd.write("mag_cal 0 0 0 1 1 1\r\n")
            serialfd.write("\r\n")
            serialfd.write("\r\n")
            print(serialfd.readline())
            sensorTest('mag_get')
            plotTwoArrays(xArray, yArray, "mag_cal_xy.png")
            print("center point max_min is ({}, {}, {})".format(sum(axisRange(xArray))/2.0, sum(axisRange(yArray))/2.0, sum(axisRange(zArray))/2.0))
            print("center point average is ({}, {}, {})".format(sum(xArray)/len(xArray), sum(yArray)/len(yArray), sum(zArray)/len(zArray)))
            print("max point is ({}, {}, {})".format(max(xArray), max(yArray), max(zArray)))
            print("min point is ({}, {}, {})".format(min(xArray), min(yArray), min(zArray)))
            print("radius point is ({}, {}, {})".format((max(xArray) - min(xArray))/2, (max(yArray) - min(yArray))/2, (max(zArray) - min(zArray))/2))
            plot3d(xArray, yArray, zArray, "mag_cal_xyz.png")
        elif cmd == "sensors":
            stest("sensors_get")

