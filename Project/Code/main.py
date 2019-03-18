import pyb
import micropython
import gc

from math import copysign, pi, radians
import utime

import cotask
import task_share

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
	mot.set_duty_cycle(0)

	while(True):
		mot.set_duty_cycle(motorL_dutycycle.get() * 100)
		yield(None)



# TODO
def motorR_fun():

	# A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
	mot = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 5, [1, 2])
	mot.set_duty_cycle(0)

	while(True):
		mot.set_duty_cycle(motorR_dutycycle.get() * 100)
		yield(None)



# TODO
def controller_fun():

	# All vectors: x_dot, theta_dot, x, theta

	# Gain matrix
	K = [0, 0.04, 0, 1.4]

	# Wheel radius (m)
	r = 0.0415
	# Ticks per revolution
	tpr = 980
	# Max motor torque (N*m)
	Tm_max = 0.6

	# Encoder objects
	enc_L = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
	enc_R = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PC7], 8, [1, 2])
	# An IMU object
	IMU = bno055.BNO055(I2C(-1, Pin('A5'), Pin('A4'), timeout=1000))

	# IMU low pass filter
	a = 0.5
	theta_act = 0
	thetadot_act = 0

	while(True):
		# Setpoint matrix
		setpoint = [xdot_set.get(), thetadot_set.get(), x_set.get(), theta_set.get()];

		# Read encoder values
		enc_read = [enc_L.read(), enc_R.read()]

		# Measured matrix
		x_act = (enc_read[0][0]-enc_read[1][0])/2 / tpr * (2*pi*r)
		xdot_act = (enc_read[0][1]-enc_read[1][1])/2 / tpr * (2*pi*r)
		theta_act = a * theta_act + (1-a) * radians(IMU.euler()[1])
		thetadot_act = a * thetadot_act + (1-a) * IMU.gyroscope()[1]
		measured = [xdot_act, thetadot_act, x_act, theta_act]

		# Calculate error
		error = [a - b for a, b in zip(setpoint, measured)]

		# Calculate motor torque
		T_m = sum(a*b for a, b in zip(error, K))

		# Duty cycle
		left_dutycycle = T_m / Tm_max + rotate_dutycycle.get()
		right_dutycycle = -T_m / Tm_max + rotate_dutycycle.get()

		# Check for stiction
		if 0.10 < abs(left_dutycycle) and abs(left_dutycycle) < 0.30:
			if not enc_read[0][1]:
				motorL_dutycycle.put(copysign(0.35, left_dutycycle))
		else:
			motorL_dutycycle.put(left_dutycycle)
		if 0.10 < abs(right_dutycycle) and abs(right_dutycycle) < 0.30:
			if not enc_read[1][1]:
				motorR_dutycycle.put(copysign(0.35, right_dutycycle))
		else:
			motorR_dutycycle.put(right_dutycycle)

		yield(None)



# TODO
def remote_fun():

	# Initialize all setpoints to 0
	x_set.put(0)
	xdot_set.put(0)
	theta_set.put(0)
	thetadot_set.put(0)

	# Set up input pins
	LF = pyb.Pin(pyb.Pin.board.D0, pyb.Pin.IN)		# left forward pin
	LR = pyb.Pin(pyb.Pin.board.D1, pyb.Pin.IN)		# left reverse pin
	RF = pyb.Pin(pyb.Pin.board.D6, pyb.Pin.IN)		# right forward pin
	RR = pyb.Pin(pyb.Pin.board.D7, pyb.Pin.IN)		# right reverse pin

	state = 0

	while(True):

		# Check joystick status
		if state == 0:

			# Left joystick status
			if LF.value() and LR.value():
				left = 0
			elif LF.value() and not LR.value():
				left = 1
			elif not LF.value() and LR.value():
				left = -1

			# Right joystick status
			if RF.value() and RR.value():
				right = 0
			elif RF.value() and not RR.value():
				right = 1
			elif not RF.value() and RR.value():
				right = -1

			# Forward / Reverse
			if left == right:
				if left == 0:		# nothing
					state = 1
				elif left == 1:		# forward
					state = 2
				elif left == -1:	# reverse
					state = 3

			# Rotation
			elif left == -right:
				if left == 1:		# turn right
					state = 4
				elif left == -1:	# turn left
					state = 5

			# Forward / Reverse with Rotation		# not implemented
			elif left != right:
				rotate_dutycycle.put(0)
				if left == 0:
					if right == 1:
						state = 6
					elif right == -1:
						state = 7
				elif right == 0:
					if left == 1:
						state = 8
					elif left == -1:
						state = 9

			yield(0)



		# Nothing
		if state == 1:
			theta_set.put(0)
			rotate_dutycycle.put(0)
			state = 0
			yield(1)



		# Forward
		if state == 2:
			theta_set.put(0.2)
			rotate_dutycycle.put(0)
			state = 0
			yield(1)



		# Reverse
		if state == 3:
			theta_set.put(-0.2)
			rotate_dutycycle.put(0)
			state = 0
			yield(3)



		# Turn right
		if state == 4:
			theta_set.put(0)
			rotate_dutycycle.put(0.15)
			state = 0
			yield(4)



		# Turn left
		if state == 5:
			theta_set.put(0)
			rotate_dutycycle.put(-0.15)
			state = 0
			yield(5)



		if state == 6:			
			state = 1		# not implemented, do nothing
			yield(6)



		if state == 7:			
			state = 1		# not implemented, do nothing
			yield(7)



		if state == 8:			
			state = 1		# not implemented, do nothing
			yield(8)



		if state == 9:			
			state = 1		# not implemented, do nothing
			yield(9)



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.



# Create inter-task communication variables
x_set = task_share.Share('i', thread_protect=False, name='Position')
xdot_set = task_share.Share('i', thread_protect=False, name='Velocity')
theta_set = task_share.Share('f', thread_protect=False, name='Angular Position')
thetadot_set = task_share.Share('f', thread_protect=False, name='Angular Velocity')

motorL_dutycycle = task_share.Share('f', thread_protect=False, name='Left Motor Duty Cycle')
motorR_dutycycle = task_share.Share('f', thread_protect=False, name='Right Motor Duty Cycle')
rotate_dutycycle = task_share.Share('f', thread_protect=False, name='Rotate Duty Cycle')



# Create tasks
motorL_task = cotask.Task(motorL_fun, name='Left Motor', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motorL_task)
motorR_task = cotask.Task(motorR_fun, name='Right Motor', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motorR_task)
controller_task = cotask.Task(controller_fun, name='Controller', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(controller_task)
remote_task = cotask.Task(remote_fun, name='Remote', priority=2,
						  period=50, profile=True, trace=False)
cotask.task_list.append(remote_task)



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
# Print the motor2_task as well
print(motor1_task.get_trace ())
print('\r\n')