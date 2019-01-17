## @file motor.py
#  Brief doc for motor.py
#
#  Detailed doc for motor.py 
#
#  @author Your Name
#
#  @copyright License Info
#
#  @date January 1, 1970
#
#  @package motor
#  Brief doc for the motor module
#
#  Detailed doc for the motor module
#
#  @author Your Name
#
#  @copyright License Info
#
#  @date January 1, 1970

import pyb

## A motor driver object
#
#  Details
#  @author Your Name
#  @copyright License Info
#  @date January 1, 1970
class Motor:

	## Constructor for motor driver
	#
	#  Detailed info on motor driver constructor
	def __init__(self):
		pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
        pinA10.high()            
        pinB4 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
        pinB5 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
        
        # Set up timer and channels for PWM
        tim3 = pyb.Timer(3, freq=20000)
        self.ch1 = tim3.channel(1, pyb.Timer.PWM, pin=pinB4)
        self.ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pinB5)

	## Sets duty cycle for motor
	#
	#  Detailed info on motor driver duty cycle function
	#
	#  @param level The desired duty cycle
    def set_duty_cycle(self,level):
        print('Setting duty cycle to ' + str(level) + '!')

        if level > 0:
            self.ch1.pulse_width_percent(level)
            self.ch2.pulse_width_percent(0)
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-level) 