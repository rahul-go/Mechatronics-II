## @file encoder.py
#  The encoder module contains the Encoder class.
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

## An encoder driver object.
#
#  The Encoder class enables the user to implement multiple encoders without
#  needing to rewrite code for each one. All encoders can run and be read from
#  independently. All encoders can be zeroed independently.
#  @author Rahul Goyal, Cameron Kao, and Harry Whinnery
#  @copyright License Info
#  @date January 24, 2019
class Encoder:
    
    ## Constructor for the encoder driver.
    #
    #  The constructor is called by passing the pin objects (as a list)
    #  corresponding to the encoder, the corresponding timer ID, and the
    #  corresponding channels (as a list). The channels should be passed with
    #  with respect to the order in which the pins objects were passed.
    #  Corresponding pins, timers, and channels can be found in the user
    #  manual of the microcontroller.
    #      
    #  @param pins Pin objects for the encoder are passed as a list to specify
    #  the pins to which the physical encoder is attached.
    #
    #  @param timer Timer ID that corresponds to the pins being used. Refer to
    #  the user manual of the microcontroller to determine the correct timer
    #  ID.
    #
    #  @param channels Channels that correspond to the pins.  The channels
    #  should be passed with with respect to the order in which the pins
    #  objects were passed. Refer to the user manual of the microcontroller to
    #  to determined the correct channel for each pin.
    def __init__(self, pins, timer, channels):
        
        print('Creating an encoder driver!')
        
        # Set up encoder pins
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

        prev_position = self.position
        self.position = self.timer.counter()
        
        delta = self.position - prev_position
        if delta > 32767:
            delta -= 65536
        elif delta < -32767:
            delta += 65536
        self.distance += delta

        return self.distance

    ## Zeros the encoder.
    #
    #  The zero function resets the timer counter, position of the motor, and
    #  distance traveled by the motor.
    def zero(self):
        self.timer.counter(0);
        self.position = 0;
        self.distance = 0;