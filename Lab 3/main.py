## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date February 07, 2019

import pyb
import micropython
import gc

import motor
import encoder
import controller
import motorcontroller

import cotask
import task_share
import print_task



# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)

# TODO
def motor1_fun():

	# A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
	mot = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
	# An encoder object
	enc = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
	# A controller object
	cont = controller.Controller(K_p=0.10)

	state = 0

	while(True):

		# Stopped
		if state == 0:
			# If key is pressed, set state to 1
			# if vcp.read() == b'\x31':
			if pos_ctrl1.get():
				state = 1
			elif step_rsp1.get():
				state = 2
			elif get_data1.get():
				state = 3
			else:
				mot.set_duty_cycle(0)	

		# Position Control
		elif state == 1:
			if pos_ctrl1.get():
				cont.set_setpoint(setpoint1.get())
				# mot.set_duty_cycle(cont.run(enc.read()))
				print_task.put(str(enc.read()))
			else:
				state = 0

		# Step Response
		elif state == 2:
			if setup:
				cont.clear_data()
				cont.set_setpoint(4000)
				enc.zero()
				stop = utime.ticks_add(utime.ticks_ms(), 1000)
				setup = False
			elif utime.ticks_diff(stop, utime.ticks_ms()) > 0:
				mot.set_duty_cycle(cont.run(enc.read()))
			else:
				step_rsp1.put(False)
				setup = True
				state = 0

		# Get Data
		elif state == 3:
			cont.get_data()
			state = 0

		yield(state)



# TODO
def motor2_fun():

	# A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
	mot = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 5, [1, 2])
	# An encoder object
	enc = encoder.Encoder([pyb.Pin.board.PC6, pyb.Pin.board.PB7], 8, [1, 2])
	# A controller object
	cont = controller.Controller(K_p=0.10)

	state = 0

	while(True):

		# Stopped
		if state == 0:
			if pos_ctrl2.get():
				state = 1
			elif step_rsp2.get():
				state = 2
			elif get_data2.get():
				state = 3
			else:
				mot.set_duty_cycle(0)

		# Position Control
		elif state == 1:
			if pos_ctrl2.get():
				cont.set_setpoint(setpoint1.get())
				mot.set_duty_cycle(cont.run(enc.read()))
			else:
				state = 0

		# Step Response
		elif state == 2:
			if setup:
				cont.clear_data()
				cont.set_setpoint(4000)
				enc.zero()
				stop = utime.ticks_add(utime.ticks_ms(), 1000)
				setup = False
			elif utime.ticks_diff(stop, utime.ticks_ms()) > 0:
				mot.set_duty_cycle(cont.run(enc.read()))
			else:
				step_rsp2.put(False)
				setup = True
				state = 0

		# Get Data
		elif state == 3:
			cont.get_data()
			state = 0

		yield(state)



def user_input():

	state = 0
	while(True):

		# Enter motor to control
		if state == 0:
			motor = input('Enter motor to control (1 or 2): ')
			if motor == 1:
				state = 1
			elif motor == 2:
				state = 2
			else:
				print('Invalid input! Try again! :)')

		# Control motor 1
		if state == 1:
			control = input('''Enter 1 for position control.
							   Enter 2 for step response.
							   ''')
			if control == 1:
				setpoint1.put(int(input('Enter setpoint: ')))
				pos_ctrl1.put(True)
			elif control == 2:
				step.rsp1.put(True)
			else:
				print('Invalid input! Try again! :)')

		# Control motor 2
		if state == 2:
			control = input('''Enter 1 for position control.
							   Enter 2 for step response.''')
			if control == 1:
				setpoint2.put(int(input('Enter setpoint: ')))
				pos_ctrl2.put(True)
			elif control == 2:
				step.rsp2.put(True)
			else:
				print('Invalid input! Try again! :)')

		yield(state)



def manual_control():
	
	state = 0
	while(True):

		# Position Control
		if state == 0:
			pos_ctrl1.put(1)
			setpoint1.put(20000)
			pos_ctrl2.put(1)
			setpoint2.put(40000)
			state = 1

		# Step Response 2
		elif state == 1:
			pass

		yield(state)



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.



# Create inter-task communication variables
pos_ctrl1 = task_share.Share('H', thread_protect=False, name='Position Control 1')
setpoint1 = task_share.Share('I', thread_protect=False, name='Setpoint 1')
step_rsp1 = task_share.Share('H', thread_protect=False, name='Step Response 1')
get_data1 = task_share.Share('H', thread_protect=False, name='Get Data 1')
pos_ctrl2 = task_share.Share('H', thread_protect=False, name='Position Control 2')
setpoint2 = task_share.Share('I', thread_protect=False, name='Setpoint 2')
step_rsp2 = task_share.Share('H', thread_protect=False, name='Step Response 2')
get_data2 = task_share.Share('H', thread_protect=False, name='Get Data 2')



# Create tasks
motor1_task = cotask.Task(motor1_fun, name='Motor 1', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motor1_task)
motor2_task = cotask.Task(motor2_fun, name='Motor 2', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(motor2_task)
# user_input = cotask.Task(motor1_fun, name='Motor 1', priority=1,
# 						  period=10, profile=True, trace=False)
# cotask.task_list.append(user_input)

# LINE BENEATH IS THE PROBLEM CODE
manual_control = cotask.Task(manual_control, name='Manual Control', priority=1,
						  period=10, profile=True, trace=False)
cotask.task_list.append(manual_control)



# Run the memory garbage collector to ensure memory is as defragmented as
# possible before the real-time scheduler is started
gc.collect()

# Run the scheduler with the chosen scheduling algorithm. Quit if any 
# character is sent through the serial por
vcp = pyb.USB_VCP()
while not vcp.any():
	cotask.task_list.pri_sched()

# Empty the comm port buffer of the character(s) just pressed
vcp.read()

# Print a table of task data and a table of shared information data
print('\n' + str (cotask.task_list) + '\n')
print(task_share.show_all ())
print(task1.get_trace ())
print('\r\n')