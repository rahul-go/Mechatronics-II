## @file main.py
#  Main creates an encoder to track the distance travelled by the motor wheel.
#  Then, it continuously prints the travelled distance of the motor ever ten
#  milliseconds.
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 24, 2019

import encoder
import pyb
import utime

# An encoder object
e = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])
while(True):
	print(e.read())
	utime.sleep_ms(10)