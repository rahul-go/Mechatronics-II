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
import utime



## A motor object
pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
m = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
## An encoder object
e = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 8, [1, 2])
## A controller object
c = controller.Controller(m, e, 30, 30)

while(True):
	motor.set_duty_cycle(controller.run(encoder.read()))
	utime.sleep_ms(50)