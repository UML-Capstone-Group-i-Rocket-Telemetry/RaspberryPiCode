import time
import board
import busio
import adafruit_l3gd20
 
# Hardware I2C setup:
I2C = busio.I2C(board.SCL, board.SDA)
SENSOR = adafruit_l3gd20.L3GD20_I2C(I2C)
 
# Hardware SPI setup:
# import digitalio
# CS = digitalio.DigitalInOut(board.D5)
# SPIB = busio.SPI(board.SCK, board.MOSI, board.MISO)
# SENSOR = adafruit_l3gd20.L3GD20_SPI(SPIB, CS)
 
while True:
    angMoment = SENSOR.gyro
    print('Angular Momentum (rad/s): {}'.format(angMoment[0]))
    print()
    time.sleep(1)