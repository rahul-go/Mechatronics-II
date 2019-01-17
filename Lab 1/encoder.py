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
    def __init__(self):
        self.t8 = pyb.Timer(8, prescaler=0, period=65535)
        self.t8.channel(1, pyb.Timer.ENC_AB, pin=pyb.Pin.board.PC6)
        self.t8.channel(2, pyb.Timer.ENC_AB, pin=pyb.Pin.board.PC7)

    ## Gets the encoder's position
    #
    #  This method returns the current position of the encoder on the wheel of the motor.
    def read(self):
        self.position = self.t8.counter()

    ## Zeros out the encoder
    #
    #  Detailed info on encoder zero function
    def zero(self):
        self.position = 0;