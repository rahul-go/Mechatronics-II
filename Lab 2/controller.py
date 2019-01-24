## @file controller.py
#  The controller module contains the Controller class.
#
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019



## A controller object.
#
#  TODO
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 31, 2019
class Controller:

	## Constructor for the controller.
	#
	#  The constructor is called by TODO
	#      
	#  @param K_p TODO
	#
	#  @param x_set TODO
	#
	#  @param motor TODO
	#
	#  @param encoder TODO
	def __init__(self, motor, encoder, K_p, x_set):
		print('Creating a controller!')
		self.motor = motor
		self.encoder = encoder
		self.K_p = K_p
		self.x_set = x_set



	## TODO
	#
	#  TODO
	def run(self):
		## X_ACT TODO     
		self.x_act = self.encoder.read()
		print(self.x_act)
		level = self.K_P * (self.x_act - self.x_set)
		self.motor.set_duty_cycle(level)