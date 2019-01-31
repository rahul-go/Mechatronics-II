## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date February 07, 2019

import micropython
import pyb
import utime

import controller
import encoder
import motor

import busy_task
import cotask
import print_task
import task_share



# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)



## A motor object
pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motor1 = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
## An encoder object
encoder1 = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
## A controller object
controller1 = controller.Controller(K_p=0.10)

def motor1_fun():
	# Step response
	while(True):
		controller1.clear_data()
		input('Press "enter" to run a step response test!')
		encoder1.zero()
		controller1.set_setpoint(encoder1.read() + 4000)
		stop = utime.ticks_add(utime.ticks_ms(), 1000)
	while(utime.ticks_diff(stop, utime.ticks_ms()) > 0):
		motor1.set_duty_cycle(controller1.run(encoder1.read()))
		utime.sleep_ms(10)
	motor1.set_duty_cycle(0)
	controller1.get_data()



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.
motor1_task = cotask.Task(motor1_fun, name = 'Motor 1', priority = 1,
						  period = 1000, profile = True, trace = False)
cotask.task_list.append(motor1_task)