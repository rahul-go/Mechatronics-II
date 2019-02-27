import bno055
from machine import I2C, Pin
import utime

i2c = I2C(-1, Pin('A5'), Pin('A4'), timeout=1000)
sensor = bno055.BNO055(i2c)

while(True):
	print('Temperature: {} degrees C'.format(sensor.temperature()))
	print('Accelerometer (m/s^2): {}'.format(sensor.accelerometer()))
	print('Magnetometer (microteslas): {}'.format(sensor.magnetometer()))
	print('Gyroscope (deg/sec): {}'.format(sensor.gyroscope()))
	print('Euler angle: {}'.format(sensor.euler()))
	print('Quaternion: {}'.format(sensor.quaternion()))
	print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration()))
	print('Gravity (m/s^2): {}'.format(sensor.gravity()))
	print()

	utime.sleep_ms(500)