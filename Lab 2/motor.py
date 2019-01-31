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
	#  Creates a motor driver by initializing GPIO pins and turning the motor
	#  off for safety. The constructor is called by passing the pin objects (as
	#  a list) corresponding to the motor, the corresponding timer ID, and the
	#  corresponding channels (as a list). The channels should be passed with
	#  respect to the order in which the pins objects were passed.
	#  Corresponding pins, timers, and channels can be found in the user manual
	#  of the microcontroller.
	#      
	#  @param pins Pin objects for the motor are passed as a list to specify
	#  the pins to which the physical motor is attached. The first pin object
	#  in the list corresponds to the first input pin, the second pin object 
	#  corresponds to the second input pin, and the third pin object
	#  correspond to the enable pin.
	#
	#  @param timer Timer ID that corresponds to the pins being used. Refer to
	#  the user manual of the microcontroller to determine the correct timer
	#  ID.
	#
	#  @param channels Channels that correspond to the pins. The first channel
	#  in the list corresponds to the first input pin, and the second channel
	#  corresponds to the second input pin. Refer to the user manual of the
	#  microcontroller to determined the correct channel for each pin.
	def __init__(self, pins, timer, channels):

		print('Creating a motor driver!')
		
		# TODO
		pins[2].high()
		
		# Set up timer and channels for PWM
		tim = pyb.Timer(timer, freq=20000)
		## Channel 1 of Timer 3
		self.ch1 = tim.channel(channels[0], pyb.Timer.PWM, pin=pins[0])
		## Channel 2 of Timer 3
		self.ch2 = tim.channel(channels[1], pyb.Timer.PWM, pin=pins[1])

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