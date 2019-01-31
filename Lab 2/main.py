## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

import pyb
import controller
import encoder
import motor
# import time		# TODO delete me!
import utime



## A motor object
pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motor = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
## An encoder object
encoder = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
## A controller object
controller = controller.Controller(0.05, 30)

# while(True):
# 	motor.set_duty_cycle(controller.run(encoder.read()))
# 	utime.sleep_ms(10)

while(True):
	controller.clear_data()
	input('Press "enter" to run a step response test!')
	stop = utime.ticks_add(utime.ticks_ms(), 5000)
	while(utime.ticks_diff(stop, utime.ticks_ms()) > 0):
		motor.set_duty_cycle(controller.run(encoder.read()))
		utime.sleep_ms(10)
	motor.set_duty_cycle(0)
	controller.get_data()