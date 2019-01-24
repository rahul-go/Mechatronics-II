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
	def __init__(self, K_p, x_set):
		print('Creating a controller!')
		self.K_p = K_p
		self.x_set = x_set



	## TODO
	#
	#  TODO
	def run(self):
		level = self.K_P * (self.x_act - self.x_set)
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
	def set_xset(self, x_set):
		## TODO
		self.x_set = x_set