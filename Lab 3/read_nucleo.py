## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

from matplotlib import pyplot
import serial
import time


port = 'COM4'



with serial.Serial(port) as ser:
	# RESET AND RUN
	# Ctrl + C
	ser.write(b'\x03')
	# Ctrl + D
	ser.write(b'\x04')
	# Wait for step response
	time.sleep(4)

	# Carriage Return
	ser.write(b'\x0D')
	time.sleep(1)
	
	lines = ser.read_all().decode().splitlines()

	# Parse data
	data = []
	for line in lines:
		# Split line, separated by commas
		line = line.split(',')
		# Try converting strings to floats
		try:
			data.append([float(line[0]), float(line[1])])
		# Skip line if ValueError exception
		except ValueError:
			print('Line parse error. Skipping ' + str(line) + '.')			

# Plot data (time: first column of data, position: second column of data)
pyplot.plot([point[0] for point in data], [point[1] for point in data])
# Title
pyplot.title('Lab 3: On Schedule, Period = 5 ms')
pyplot.xlabel('Time (milliseconds)')			# x-Axis
pyplot.ylabel('Position (encoder ticks)')		# y-Axis
pyplot.xlim([0, 500])
# pyplot.annotate(str(data[len(data)-1][1]), (500, data[len(data)-1][1]))