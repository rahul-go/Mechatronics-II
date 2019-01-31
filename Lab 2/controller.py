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
	#  @param setpoint TODO
	def __init__(self, K_p, setpoint):
		print('Creating a controller!')
		self.K_p = K_p
		self.setpoint = setpoint



	## TODO
	#
	#  TODO
	def run(self, location):
		level = self.K_P * (self.location - self.setpoint)
		if level > 100:
			return 100
		elif level < -100: 
			return -100
		return level



	## TODO
	#
	#  TODO
	def set_Kp(self, K_p):
		## TODO
		self.K_p = K_p



	## TODO
	#
	#  TODO
	def set_xset(self, setpoint):
		## TODO
		self.setpoint = setpoint