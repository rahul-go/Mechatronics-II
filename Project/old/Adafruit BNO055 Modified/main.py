import time
# import board
# import busio
# import adafruit_bno055

# i2c = busio.I2C(board.SCL, board.SDA)
# sensor = adafruit_bno055.BNO055(i2c)

import pyb
import machine
import bno055

i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate = 100000)
print(i2c.scan())
sensor = bno055.BNO055(i2c)

while True:
	print('Temperature: {} degrees C'.format(sensor.temperature.get()))
	print('Accelerometer (m/s^2): {}'.format(sensor.accelerometer.get()))
	print('Magnetometer (microteslas): {}'.format(sensor.magnetometer.get()))
	print('Gyroscope (deg/sec): {}'.format(sensor.gyroscope.get()))
	print('Euler angle: {}'.format(sensor.euler.get()))
	print('Quaternion: {}'.format(sensor.quaternion.get()))
	print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration.get()))
	print('Gravity (m/s^2): {}'.format(sensor.gravity.get()))
	print()

	time.sleep(1)