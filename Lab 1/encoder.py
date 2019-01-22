## @file encoder.py
#  Brief doc for encoder.py
#
#  Detailed doc for encoder.py 
#
#  @author Your Name
#
#  @copyright License Info
#
#  @date January 1, 1970
#
#  @package encoder
#  Brief doc for the encoder module
#
#  Detailed doc for the encoder module
#
#  @author Your Name
#
#  @copyright License Info
#
#  @date January 1, 1970

import pyb

## An encoder driver object
#
#  Details
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 1, 1970

class Encoder:
    
    ## Constructor for encoder driver
    #
    #  Detailed info on encoder driver constructor
    def __init__(self, timer, channels, pins):
        
        # Set up encoder pins
        self.timer = pyb.Timer(timer, prescaler=0, period=65535)
        self.timer.channel(channels[0], pyb.Timer.ENC_AB, pins[0])
        self.timer.channel(channels[1], pyb.Timer.ENC_AB, pins[1]) 
        
        # Initialize position and offset to 0
        self.zero()

    ## Gets the encoder's position
    #
    #  This method returns the current position of the encoder on the wheel of the motor.
    def read(self):

        prev_position = self.position
        self.position = self.timer.counter() - self.offset
        
        delta = self.position - prev_position
        if delta > 2000:
            delta -= 4000
        elif delta < -2000:
            delta += 4000
        self.distance += delta

        return self.distance

    ## Zeros out the encoder
    #
    #  Detailed info on encoder zero function
    def zero(self):

        self.position = 0;
        self.distance = 0;
        self.offset = self.timer.counter();