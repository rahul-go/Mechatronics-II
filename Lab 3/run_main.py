## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

import serial
import time


port = 'COM3'



with serial.Serial(port) as ser:
	# RESET AND RUN
	# Ctrl + C
	ser.write(b'\x03')
	# Ctrl + D
	ser.write(b'\x04')
	# Carriage Return
	ser.write(b'\x0D')
	# Write a 1 
	ser.write(b'\x31')
	# Carriage Return
	ser.write(b'\x0D')