## @file encoder.py
#  The main function of the Encoder file is to enable multiple encoder objects
#  to be made. Each encoder should be able to return the correct position 
#  of the motor encoder when the "read()" function is called. Each encoder 
#  should also be able to zero or resets it's position by calling the zero
#  function.
#
#  The Encoder class may be used to create encoder multiple encoder objects.
#  The "__init__" function will be used by passing in the pin locations for 
#  the encoder accordingly, the timer correlating to the the pin locations, 
#  and the two channels correlating to the pin locations. The correct pin 
#  locations and other correlating parameters can be found in the user manual.
#  The "read()" function will be used to return the position of the motor 
#  encoder wheel using a position between 0 and 65535. The "zero()" function 
#  will cause the encoder to reset its position to 0. 
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 24, 2019

import pyb

## An encoder driver object
#
#  Details
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 24, 2019

class Encoder:
    
    ## Constructor for encoder driver
    #
    #  The "__init__" constructor will be used by passing in the pin locations for 
    #  the encoder accordingly, the timer correlating to the the pin locations, 
    #  and the two channels correlating to the pin locations. The correct pin 
    #  locations and other correlating parameters can be found in the user manual.
    #      
    #  @param pins Pin objects for the encoder are passed through this parameter
    #  in order to specify which pins are reading the encoder.
    #
    #  @param timer Timer object correlates to the pins being used. Which timer
    #  to use can be found using the user manual.
    #
    #  @param channels Channels object correlates to the pins being used for the
    #  encoder as well, and can also be found in the user manual.
    #
    def __init__(self, pins, timer, channels):
        
        print('Creating an encoder driver!')
        
        # Set up encoder pins
        self.timer = pyb.Timer(timer, prescaler=0, period=65535)
        self.timer.channel(channels[0], pyb.Timer.ENC_AB, pin = pins[0])
        self.timer.channel(channels[1], pyb.Timer.ENC_AB, pin = pins[1]) 
        
        # Initialize position, distance, and timer counter to 0
        self.zero()

    ## Gets the encoder's position
    #
    # The "read()" function will be used to return the position of the motor 
    # encoder wheel using a position between 0 and 65535.
    def read(self):

        prev_position = self.position
        self.position = self.timer.counter()
        
        delta = self.position - prev_position
        if delta > 32767:
            delta -= 65536
        elif delta < -32767:
            delta += 65536
        self.distance += delta

        return self.distance

    ## Zeros out the encoder
    #
    #  The zero function makes resets the position to zero, sets the distance to zero, and sets the timer counter to zero.
    def zero(self):
        self.timer.counter(0);
        self.position = 0;
        self.distance = 0;