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



with serial.Serial(port) as rahul:
	# RESET AND RUN
	# Ctrl + C
	rahul.write(b'\x03')
	# Ctrl + D
	rahul.write(b'\x04')
	# Carriage Return
	rahul.write(b'\x0D')

	# READ AND PARSE
	time.sleep(4)
	# print(rahul.read_all())
	
	lines = rahul.read_all().decode().splitlines()

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
pyplot.title('Lab 2: In Control')				# Title
pyplot.xlabel('Time (milliseconds)')			# x-Axis
pyplot.ylabel('Position (encoder ticks)')		# y-Axis