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

	# READ AND PARSE
	time.sleep(4)
	
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
pyplot.title('Lab 2: In Control, K_p = 0.10')
pyplot.xlabel('Time (milliseconds)')			# x-Axis
pyplot.ylabel('Position (encoder ticks)')		# y-Axis
pyplot.xlim([0, 500])
# pyplot.annotate(str(data[len(data)-1][1]), (500, data[len(data)-1][1]))