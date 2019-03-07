## @file controller.py
#  The controller module contains the Controller class.
#
#  The controller class is a general PID controller. The initialization class
#  consists of setting a proportional gain and setpoint. The controller must
#  then be repeatedly called and given a measurement of the value being
#  controlled. The controller will then return a value to be output to the
#  controller. As an added functionality, the controller records times and
#  measurements.
#  
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

import utime
import print_task

## A controller object.
#
#  The controller class is a general PID controller. The initialization class
#  consists of setting a proportional gain and setpoint. The controller must
#  then be repeatedly called and given a measurement of the value being
#  controlled. The controller will then return a value to be output to the
#  controller. As an added functionality, the controller records times and
#  measurements.
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
	#  @param K_i Integral gain constant for controller.
	#
	#  @param K_d Derivative gain constant for controller.
	#
	#  @param setpoint Initial setpoint for controller. Determines where the 
	# controller will try to go when the run function is called. 
	def __init__(self, K_p=1, K_i=0, K_d=0, setpoint=0):
		print('Creating a controller!')
		
		## Creates instance variables for K_p, K_i, K_d, error, e_sum, e_der,
		#  t_old, setpoint, time and, vals. Data will be later put into time
		#  and vals, where time is the time at which the run function is called
		#  and vals is the measurement input.
		self.K_p = K_p
		self.K_i = K_i
		self.K_d = K_d
		self.error = 0
		self.e_sum = 0
		self.e_der = 0
		self.t_old = utime.ticks_us()
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
		#  contains the time and corresponding value, and returns it as a list.
		return list(zip(self.time, self.vals))



	## Returns output value to actuator.
	#
	#  The "run()" function passes the sensor measurement and outputs an 
	#  actuation value based on the K_p and setpoint. The avtuation value 
	#  saturates at -100 and 100.
	def run(self, measurement):
		
		## Adds the current time, as read by utime.ticks_ms() to the end of the 
		#  time list.
		# self.time.append(utime.ticks_ms())
		
		## Adds the current measurement to the end of the vals list.
		# self.vals.append(measurement)

		## The actuation value is the difference between the setpoint and 
		#  measurement values multiplied by the K_p value. If this value is 
		#  greater than 100, it is set to 100. If it is less than -100 it is 
		#  set to -100. This saturation prevents the controller from returning
		#  an actuation value that is too extreme.
		t_new = utime.tick_us()
		dt = t_new - self.t_old
		self.t_old = t_new

		self.e_der = (self.error - (self.setpoint - measurement)) / dt
		self.error = self.setpoint - measurement
		self.e_sum += self.error
		
		actuation = self.K_p * error + self.K_i * self.e_sum + self.K_d * e_der
		if actuation > 100:
			return 100
		elif actuation < -100:
			return -100
		return actuation



	## The "set_Kp()" function sets the proportional gain value, K_p.
	def set_Kp(self, K_p):
		## Sets the instance variable of K_p to the function input.
		self.K_p = K_p



	## The "set_Ki()" function sets the integral gain value, K_i.
	def set_Ki(self, K_i):
		## Sets the instance variable of K_i to the function input.
		self.K_i = K_i



	## The "set_Kd()" function sets the derivative gain value, K_d.	
	def set_Kd(self, K_d):
		## Sets the instance variable of K_d to the function input.
		self.K_d = K_d



	## The "set_setpoint()" function sets the setpoint value.
	def set_setpoint(self, setpoint):
		## Sets the instance variable of setpoint to the function input.
		self.setpoint = setpoint