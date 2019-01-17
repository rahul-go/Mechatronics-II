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
#  @author Your Name
#  @copyright License Info
#  @date January 1, 1970
class Encoder:
    
    ## Constructor for encoder driver
    #
    #  Detailed info on encoder driver constructor
    def __init__(self, timer, chA, chB, pinA, pinB):
        
        # Set up encoder pins
        self.timer = pyb.Timer(timer, prescaler=0, period=65535)
        # FIX PIN
        self.timer.channel(chA, pyb.Timer.ENC_AB, pin=pyb.Pin.board.PB6)
        # FIX PIN
        self.timer.channel(chB, pyb.Timer.ENC_AB, pin=pyb.Pin.board.PB7) 
        
        # Initialize position and offset to 0
        self.zero()          

    ## Gets the encoder's position
    #
    #  This method returns the current position of the encoder on the wheel of the motor.
    def read(self):

        prev_position = self.position
        self.position = self.timer.counter() - self.offset
        
        delta = self.position - prev_position
        if delta > 32767:
            pass
        elif delta < -32767:
            pass
        self.distance += delta

    ## Zeros out the encoder
    #
    #  Detailed info on encoder zero function
    def zero(self):
        self.position = 0;
        self.distance = 0;
        self.offset = self.timer.counter();