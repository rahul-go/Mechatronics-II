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
		self.timer.channel(channels[0], pyb.Timer.ENC_AB, pin = pins[0])
		self.timer.channel(channels[1], pyb.Timer.ENC_AB, pin = pins[1]) 
		
		# Initialize position, distance, and timer counter to 0
		self.zero()



	## Gets the encoder's traveled distance.
	#
	#  The "read()" function is used to return the distance traveled by the
	#  motor in terms of encoder ticks. The function handles underflow and
	#  overflow in the 16-bit timer counter by calculating the more likely
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
		delta = self.position - prev_position
		if delta > 32767:
			delta -= 65536
		elif delta < -32767:
			delta += 65536
		## Distance traveled by the motor (in encoder ticks) relative to the
		#  current zero. Accounts for timer counter underflow/overflow.
		self.distance += delta

		return self.distance



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
		self.position = 0;
		## Distance traveled by the motor (in encoder ticks) relative to the
		#  current zero. Accounts for timer counter underflow/overflow.
		self.distance = 0;