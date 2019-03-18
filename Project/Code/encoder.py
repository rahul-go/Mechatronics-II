## @file encoder.py
#  The encoder module contains the Encoder class.
#
#  The Encoder class enables the user to implement multiple encoders without
#  needing to rewrite code for each one. All encoders can run and be read from
#  independently. All encoders can be zeroed independently. The class also
#  attempts to handle timer counter underflow/overflow errors.
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 24, 2019

import pyb
import utime

## An encoder driver object.
#
#  The Encoder class enables the user to implement multiple encoders without
#  needing to rewrite code for each one. All encoders can run and be read from
#  independently. All encoders can be zeroed independently. The class also
#  attempts to handle timer counter underflow/overflow errors.
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 24, 2019
class Encoder:
	
	## Constructor for the encoder driver.
	#
	#  The constructor is called by passing the pin objects (as a list)
	#  corresponding to the encoder, the corresponding timer ID, and the
	#  corresponding channels (as a list). The channels should be passed with
	#  respect to the order in which the pins objects were passed.
	#  Corresponding pins, timers, and channels can be found in the user manual
	#  of the microcontroller.
	#      
	#  @param pins Pin objects for the encoder are passed as a list to specify
	#  the pins to which the physical encoder is attached.
	#
	#  @param timer Timer ID that corresponds to the pins being used. Refer to
	#  the user manual of the microcontroller to determine the correct timer
	#  ID.
	#
	#  @param channels Channels that correspond to the pins. The channels
	#  should be passed with with respect to the order in which the pins
	#  objects were passed. Refer to the user manual of the microcontroller to
	#  to determined the correct channel for each pin.
	def __init__(self, pins, timer, channels):
		
		print('Creating an encoder driver!')
		
		# Set up encoder pins
		## Timer object, with the provided timer ID, prescaler=0, and
		#  period=65535.
		self.timer = pyb.Timer(timer, prescaler=0, period=65535)
		self.timer.channel(channels[0], pyb.Timer.ENC_AB, pin=pins[0])
		self.timer.channel(channels[1], pyb.Timer.ENC_AB, pin=pins[1]) 
		
		# Initialize position, distance, and timer counter to 0
		self.zero()



	## Gets the encoder's traveled distance.
	#
	#  The "read()" function is used to return the distance traveled by the
	#  motor in units of encoder ticks, as well as the velocity, which is in 
	#  units of encoder ticks/second as a list. The function handles underflow
	#  and overflow in the 16-bit timer counter by calculating the more likely
	#  direction of travel in the case of large changes in value. This is most
	#  effective and accurate when the read function is called quickly enough.
	#  "Quickly" is determined as a function of motor speed; a motor spinning
	#  more quickly will require the read() function to be called more
	#  frequently for underflow/overflow to be handled properly.
	
	def read(self):

		## Position of the motor the last time read() was called, according to
		#  to the timer counter.
		prev_position = self.position
		## Position of the motor in the current read() call, according to the 
		#  timer counter.
		self.position = self.timer.counter()
		## Change in position from the last read() call, according to the timer
		#  counter.
		delta_pos = self.position - prev_position
		if delta_pos > 32767:
			delta_pos -= 65536
		elif delta_pos < -32767:
			delta_pos += 65536

		## Stores the previous value for time
		prev_time = self.time
		## Fetches the current time
		self.time = utime.ticks_us()
		## Determines how much time has passed by subtracting the previous time
		#  from the current one
		delta_time = self.time - prev_time

		## Distance traveled by the motor (in encoder ticks) relative to the
		#  current zero. Accounts for timer counter underflow/overflow.
		self.distance += delta_pos

		## Calculates the velocity in ticks/s by dividing the change in 
		#  position by change in time. The order of operations is chosen 
		#  such that the rounding caused by the integer division is not 
		#  multiplied. 
		velocity = 1000000 * delta_pos // delta_time

		return [self.distance, velocity]



	## Zeroes the encoder.
	#
	#  The zero function resets the timer counter, position of the motor, and
	#  distance traveled by the motor. If the motor hasn't moved, a subsquent
	#  call of the read() function will return 0. All subsequent calls of the
	#  read() function will return distance traveled (in encoder ticks)
	#  relative to this new zero position.
	def zero(self):
		self.timer.counter(0);
		## Position of the motor in the current read() call, according to the 
		#  timer counter.
		self.position = self.timer.counter();
		## Sets the time variable to the current value of time.ticks_us(), 
		#  which is an arbitrary reference point.
		self.time = utime.ticks_us();
		## Distance traveled by the motor (in encoder ticks) relative to the
		#  current zero. Accounts for timer counter underflow/overflow.
		self.distance = 0;