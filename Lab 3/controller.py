## @file controller.py
#  The controller module contains the Controller class.
#
#  The controller class is a general proportional controller. The 
#  initialization consists of setting a proportional gain and setpoint. The 
#  controller must then be repeatedly called and given a measurement of the 
#  value being controlled. The controller will then return a value to be 
#  output to the controller. As an added functionality, the controller 
#  records its time and output.
#  
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

import utime

## A controller object.
#
#  The controller class is a general proportional controller. The 
#  initialization consists of setting a proportional gain and setpoint. The 
#  controller must then be repeatedly called and given a measurement of the 
#  value being controlled. The controller will then return a value to be 
#  output to the controller. As an added functionality, the controller 
#  records its time and output.
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 31, 2019
class Controller:

	## Constructor for the controller.
	#
	#  The constructor is called by passing K_p and the setpoint. The 
	#  constructor then saves these values as variables. It also creates empty 
	#  arrays for the controller’s time and values.
	#      
	#  @param K_p Proportional gain constant for controller. 
	#
	#  @param setpoint Initial sepoint for controller. Determines where the 
	# controller will try to go when the run function is called. 
	def __init__(self, K_p=1, setpoint=0):
		print('Creating a controller!')
		
		## Creates instance variables for K_p, setpoint, time and vals. Data 
		#  will be later put into time and vals, where time is the time passed
		#  and vals is the input measurement.
		self.K_p = K_p
		self.setpoint = setpoint
		self.time = []
		self.vals = []



	## Clears the data in instance variables time and vals.
	#
	#  The "clear_data" function is used whenever the user would like to clear
	#  the existing time and vals variables.
	def clear_data(self):  
		self.time = []
		self.vals = []



	## Prints time and value data to the console.
	#
	#  When the "get_data()" function is called, it offsets the time data 
	#  by the inital value for time, such that the time data begins at 0. It 
	#  then prints the time and value data to the console. 
	def get_data(self):
		## Offsets time data by the initial value for time, such that the time
		#  data begins at 0.
		self.time = [t - self.time[0] for t in self.time]
		## Combines time and value lists into a list of lists, where each list 
		#  contains the time and corresponding value.
		data = zip(self.time, self.vals)
		#  Prints each value in the data list to the console.
		for datum in data:
			print(str(datum[0]) + ', ' + str(datum[1]))



	## Returns output value to actuator.
	#
	#  The "run()" function passes the sensor measurement and outputs an 
	#  actuation value based on the K_p and setpoint. The avtuation value 
	#  saturates at -100 and 100.
	def run(self, measurement):
		
		## Adds the current time, as read by utime.ticks_ms() to the end of the 
		#  time list.
		self.time.append(utime.ticks_ms())
		
		## Adds the current measurement to the end of the vals list.
		self.vals.append(measurement)

		## The actuaion value is the difference between the setpoint and 
		#  measurement values multiplied by the K_p value. If this value is 
		#  greater than 100, it is set to 100. If it is less than -100 it is 
		#  set to -100. This saturation prevents the controller from returning
		#  an actuation value that is too extreme.
		actuation = self.K_p * (self.setpoint - measurement)
		if actuation > 100:
			return 100
		elif actuation < -100:
			return -100
		return actuation



	## The "set_Kp()" function sets the proportional gain value, K_p.
	def set_Kp(self, K_p):
		## Sets the instance variable of K_p to the function input.
		self.K_p = K_p



	## The "set_setpoint()" function sets the setpoint value.
	def set_setpoint(self, setpoint):
		## Sets the instance variable of setpoint to the function input.
		self.setpoint = setpoint