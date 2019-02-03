## @file motorcontroller.py
#  The motorcontroller module contains the MotorController class.
#
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date February 07, 2019

import utime

## An motor controller object.
#
#  TODO
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date February 07, 2019
class MotorController:

	## Constructor for the motor controller.
	#
	#  TODO (pass in motor, encoder, controller OBJECTS)
	def __init__(self, motor, encoder, controller):

		print('Creating a motor controller!')

		self.motor = motor
		self.encoder = encoder
		self.controller = controller



	## TODO
	#
	#  TODO
	def run(self):
		self.motor.set_duty_cycle(self.controller.run(self.encoder.read()))



	## TODO
	#
	#  TODO
	def step_response(self):
		# Step response
		self.controller.clear_data()
		self.controller.set_setpoint(4000)
		self.encoder.zero()
		stop = utime.ticks_add(utime.ticks_ms(), 1000)
		while(utime.ticks_diff(stop, utime.ticks_ms()) > 0):
			self.run()
		self.motor.set_duty_cycle(0)
		self.controller.get_data()