## @file main.py
#  The main creates a motor driver in order to control how fast the motor spins
#  and in what direction. Main also creates an encoder in order to track where
#  the position of the motor encoder and allows the motor position to be reset.
#  Main will then continuously print out the position of the motor every ten
#  seconds.
#
#  The Motor Driver "m" will be created passing in no parameters. This is what
#  will be controlling both how fast the motor is running, and in what direction
#  it will be running in. The Encoder "e" will be created passing in the pin
#  the pin locations for the encoder accordingly, the timer correlating to the
#  the pin locations, and the two channels correlating to the pin locations. 
#  The correct pin locations and other correlating parameters can be found in
#  the user manual. Main will then enter an infinite loop where it will 
#  continually print the call of the "read()" function for the encoder object. 
#  This function will return the position of the motor encoder wheel, which
#  will be a value between 0 and 65535. Main will then use the sleep function
#  to stop the infinite while loop for 10ms.
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 24, 2019

import encoder
import pyb
import utime

## An encoder object
e = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])

while(True):
	print(e.read())
	utime.sleep_ms(10)