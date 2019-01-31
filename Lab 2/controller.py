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

import utime

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
		self.time = []
		self.vals = []



	## TODO
	#
	#  TODO
	def clear_data(self):
		self.time = []
		self.vals = []



	## TODO
	#
	#  TODO
	def get_data(self):
		t_0 = self.time[0]
		
		self.time = [t - self.time[0] for t in self.time]
		data = zip(self.time, self.vals)
		for datum in data:
			print(datum)



	## TODO
	#
	#  TODO
	def run(self, measurement):
		self.time.append(utime.ticks_ms())
		self.vals.append(measurement)
		print(measurement)

		actuation = self.K_p * (self.setpoint - measurement)
		if actuation > 100:
			return 100
		elif actuation < -100:
			return -100
		return actuation



	## TODO
	#
	#  TODO
	def set_Kp(self, K_p):
		## TODO
		self.K_p = K_p



	## TODO
	#
	#  TODO
	def set_setpoint(self, setpoint):
		## TODO
		self.setpoint = setpoint