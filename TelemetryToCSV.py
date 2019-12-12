#! /usr/bin/env python
#from subprocess import call
#call([‘espeak “Welcome to the world of Robots” 2>/dev/null’], shell=True)
import time
from datetime import datetime
import board
import busio
import csv
#gyro lib
import adafruit_l3gd20
#Altimeter lib
import adafruit_mpl3115a2
#Accelerometer lib
import adafruit_mma8451
#Temp Sensor Lib
import adafruit_mcp9808

I2C = busio.I2C(board.SCL, board.SDA)
# Initialize the  Gyro
Gyro = adafruit_l3gd20.L3GD20_I2C(I2C)
# Initialize the Altimeter
Altimeter = adafruit_mpl3115a2.MPL3115A2(I2C)
# Initialize the Accelerometer
Accelerometer = adafruit_mma8451.MMA8451(I2C)
#Initialize the Temp Sensor
TempSensor = adafruit_mcp9808.MCP9808(I2C)
#create unique data file name from dat and time
DateTime = datetime.now()
FileName = DateTime.strftime("%m-%d-%Y_%Hh%Mm%Ss_FlightFile.csv")
#index value for each axis on gyro
xAxis = 0
yAxis = 1
zAxis = 2
#time keeping variables
currTime = 0
flightTime = 0.00
# 1 = 1 per sec, .1 = 10 per second, .01 = 100 per second
# don't do more than 100 per second
sampleRate = .1
#sets relative altitude to start up height (Sets start altitude to zero)
#take 10 samples  over 10 seconds and use average as starting pressure
avgGndPress = 0
for x in range(0, 10):
    print('Calabrating Ground Pressure {}'.format(x))
    avgGndPress = avgGndPress + Altimeter.pressure
    time.sleep(.1)
avgGndPress = avgGndPress / 10.000
Altimeter.sealevel_pressure = int(avgGndPress)
print('Ground Pressure has been calibrated')
acceleration = Accelerometer.acceleration
prevAccel = acceleration
currTime = time.time()
while True:
    acceleration = Accelerometer.acceleration
    orientation = Accelerometer.orientation
    if orientation == adafruit_mma8451.PL_PUF:
        orientationStr = 'Portrait, up, front'
    elif orientation == adafruit_mma8451.PL_PUB:
        orientationStr = 'Portrait, up, back'
    elif orientation == adafruit_mma8451.PL_PDF:
        orientationStr = 'Portrait, down, front'
    elif orientation == adafruit_mma8451.PL_PDB:
        orientationStr = 'Portrait, down, back'
    elif orientation == adafruit_mma8451.PL_LRF:
        orientationStr = 'Landscape, right, front'
    elif orientation == adafruit_mma8451.PL_LRB:
        orientationStr = 'Landscape, right, back'
    elif orientation == adafruit_mma8451.PL_LLF:
        orientationStr = 'Landscape, left, front'
    elif orientation == adafruit_mma8451.PL_LLB:
        orientationStr = 'Landscape, left, back'
    #this commented code is if you wanted to something at less than the sample rate
    #if float(flightTime * .1).is_integer():
        #print('Time: {} sec' .format(flightTime))
        #print('Acceleration x axis: {0:0.3f} m/s^2'.format(acceleration[xAxis]))
    tempC = TempSensor.temperature
    tempF = tempC * 9 / 5 + 32
    pressure = Altimeter.pressure
    #print('Pressure: {0:0.3f} pascals'.format(pressure))
    altitude = Altimeter.altitude
    #print('Altitude: {0:0.3f} meters'.format(altitude))
    #temperature = Altimeter.temperature
    #print('Temperature: {0:0.3f} degrees Celsius'.format(temperature))
    angMoment = Gyro.gyro
    #print('Angular Momentum x axis (rad/s): {}'.format(angMoment[xAxis]))
    #create csv row
    rowCSV = [str(flightTime), str(acceleration[xAxis]), str(acceleration[yAxis]),
              str(acceleration[zAxis]), orientationStr, str(tempC), str(tempF),
              str(pressure), str(altitude), str(angMoment[xAxis]), str(angMoment[yAxis]),
              str(angMoment[zAxis])]
    with open(FileName,'a') as fd:
        writer = csv.writer(fd, delimiter=';')
        writer.writerow(rowCSV)
    while(time.time() < currTime + sampleRate):
        continue
    currTime = time.time()
    flightTime = round(flightTime + sampleRate, 3)
