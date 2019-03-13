import pyb
import micropython
import gc

import utime

import cotask
import task_share
import print_task

import motor
import encoder
import bno055
from machine import I2C, Pin



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



# TODO
def controller_fun():

	# All vectors: x_dot, theta_dot, x, theta

	# Gain matrix
	K = [1, 1, 1, 1]

	# Encoder objects
	enc_L = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
	enc_R = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])

	# An IMU object
	IMU = bno055.BNO055(I2C(-1, Pin('A5'), Pin('A4'), timeout=1000))

	while(True):
		# Setpoint matrix
		setpoint = [xdot_set.get(), thetadot_set.get(), x_set.get(), theta_set.get()];

		# Measured matrix
		x_act = (encL.read()[0] + encR.read()[0]) / 2
		xdot_act = (encL.read()[1] + encR.read()[1]) / 2
		theta_act = IMU.euler()[1]
		thetadot_act = IMU.gyroscope()[1]
		measured = [xdot_act, thetadot_act, x_act, theta_act]

		# Calculate error
		error = [a - b for a, b in zip(setpoint, measured)]

		# Calculate motor torque
		T_m = sum(a*b for a, b in zip(error, K))

		yield(None)



# TODO
def routine_fun():

	x_set.put(0);
	xdot_set.put(0);
	theta_set.put(0);
	thetadot_set.put(0);

	while(True):
		yield(None)



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.



# Create inter-task communication variables
x_set = task_share.Share('i', thread_protect=False, name='Position')
xdot_set = task_share.Share('i', thread_protect=False, name='Velocity')
theta_set = task_share.Share('i', thread_protect=False, name='Angular Position')
thetadot_set = task_share.Share('i', thread_protect=False, name='Angular Velocity')



# Create tasks
motorL_task = cotask.Task(motor1_fun, name='Left Motor', priority=2,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motorL_task)
motorR_task = cotask.Task(motor2_fun, name='Right Motor', priority=2,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motorR_task)
controller_task = cotask.Task(controller_fun, name='Controller', priority=2,
						  period=10, profile=True, trace=False)
cotask.task_list.append(controller_task)
routine_task = cotask.Task(routine_fun, name='Routine', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(routine_task)



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