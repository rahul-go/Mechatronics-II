## @file main.py
#  Main creates an encoder to track the distance travelled by the motor wheel.
#  Then, it continuously prints the travelled distance of the motor ever ten
#  milliseconds.
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

print('hello')
encoder = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])
motor = motor.MotorDriver()
controller = controller.Controller(K_P = 1, x_0 = 1, motor, encoder)

while(True):
	controller.run()
	utime.sleep_ms(10)