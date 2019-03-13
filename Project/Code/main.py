import pyb
import micropython
import gc

# import numpy
import utime

import motor
import encoder
# import controller

import bno055
from machine import I2C, Pin

import cotask
import task_share
import print_task



# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf(100)

# TODO
def motorL_fun():
	
	# A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
	mot = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
	
	while(True):
		print(str(enc.read()[0]))
		yield(None)



# TODO
def motorR_fun():

	# A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
	mot = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 5, [1, 2])

	while(True):
		yield(None)



def controller():

	# All vectors: x_dot, theta_dot, x, theta

	# Gain matrix
	K = [1, 1, 1, 1]

	# A matrix
	A11 = 
	A12 = 
	A14 = 
	A21 = 
	A22 = 
	A24 = 
	A = [[0]]

	# B matrix

	# Encoder objects
	enc_L = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
	enc_R = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])

	while(True):
		# Setpoint matrix
		setpoint = [x_dot.get(), theta_dot.get(), x.get(), theta.get()];

		# Calculate error
		error = [a - b for a, b in zip(setpoint, x_t)]

		# Calculate motor torque
		T_m = sum(a*b for a, b in zip(error, K))

def routine():

	x.put(0);
	x_dot.put(0);
	theta.put(0);
	theta_dot.put(0);

	while(True):
		yield(None)



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.



# Create inter-task communication variables
x = task_share.Share('i', thread_protect=False, name='Position')
x_dot = task_share.Share('i', thread_protect=False, name='Velocity')
theta = task_share.Share('i', thread_protect=False, name='Angle')
theta_dot = task_share.Share('i', thread_protect=False, name='Angular Velocity')



# Create tasks
motor1_task = cotask.Task(motor1_fun, name='Motor 1', priority=2,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motor1_task)
motor2_task = cotask.Task(motor2_fun, name='Motor 2', priority=2,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motor2_task)



# Run the memory garbage collector to ensure memory is as defragmented as
# possible before the real-time scheduler is started
gc.collect()

# Run the scheduler with the chosen scheduling algorithm. Quit if any 
# character is sent through the serial port
vcp = pyb.USB_VCP()
while not vcp.any():
	cotask.task_list.pri_sched()

# Empty the comm port buffer of the character(s) just pressed
vcp.read()

# Print a table of task data and a table of shared information data
print('\n' + str (cotask.task_list) + '\n')
print(task_share.show_all ())
# print the motor2_task as well
print(motor1_task.get_trace ())
print('\r\n')



# =============================================================================