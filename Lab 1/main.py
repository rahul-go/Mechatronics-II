## @file main.py
#  Brief doc for main.py
#
#  Detailed doc for main.py 
#
#  @author Your Name
#
#  @copyright License Info
#
#  @date January 1, 1970

import encoder
import motor
import pyb
import utime

## A motor driver object
m = motor.MotorDriver()
## An encoder object
e = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])

while(True):
	print(e.read())
	utime.sleep_ms(10)