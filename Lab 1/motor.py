## @file motor.py
#  The motor module contains the MotorDriver class.
#
#  The MotorDriver class implements a motor driver for the ME405 board. At any
#  point while the motor is running, the user can use this class to modify the
#  duty cycle of the signal and the motor will react appropriately.
#
#  @author Harry Whinnery, Rahul Goyal, Cameron Kao
#
#  @copyright License Info
#
#  @date January 24, 2019
#
#  @package MotorDriver

import pyb
import time

## A motor driver object
#
#  The MotorDriver class implements a motor driver for the ME405 board. At any
#  point while the motor is running, the user can use this class to modify the
#  duty cycle of the signal and the motor will react appropriately.
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#  @copyright License Info
#  @date January 24, 2019
class MotorDriver:
	
	## Constructor for motor driver
	#
	# Creates a motor driver by initializing GPIO
	# pins and turning the motor off for safety.
	def __init__(self):

		print('Creating a motor driver!')
		
		# Set pins to output
		pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
		pinA10.high()            
		pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
		pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
		
		# Set up timer and channels for PWM
		tim3 = pyb.Timer(3, freq=20000)
		self.ch1 = tim3.channel(1, pyb.Timer.PWM, pin=pinB4)
		self.ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pinB5)

		# Set duty cycle to 0.
		self.set_duty_cycle(0)


	## Sets duty cycle for motor
	#
	#  This method sets the duty cycle to be sent
	#  to the motor to the given level. Positive values
	#  cause torque in one direction, negative values
	#  in the opposite direction.
	#
	#  @param level A signed integer holding the duty
	#  cycle of the voltage sent to the motor.
	#  Input a number between -100 and 100.
	def set_duty_cycle(self, level):
		
		print('Setting duty cycle to ' + str(level) + '!')

		if level > 0:
			self.ch1.pulse_width_percent(level)
			self.ch2.pulse_width_percent(0)
		else:
			self.ch1.pulse_width_percent(0)
			self.ch2.pulse_width_percent(-level)



if __name__ == '__main__':

	# Creates motor driver
	mo_bamba = MotorDriver()
	
	# Set duty cycle to +50%
	mo_bamba.set_duty_cycle(50)
	time.sleep(5)
	
	# Set duty cycle to -50%
	mo_bamba.set_duty_cycle(-50)
	time.sleep(5)
	
	# Set duty cycle to 0%
	mo_bamba.set_duty_cycle(0)
	time.sleep(5)