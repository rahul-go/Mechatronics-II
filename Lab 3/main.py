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

import motor
import encoder
import controller
import motorcontroller

import cotask
import task_share
import print_task
import busy_task



# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)


vcp = pyb.USB_VCP ()

# TODO
def motor1_fun():
	## A motor object
	pinENA = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
	pinIN1A = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
	pinIN2A = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
	motor1 = motor.MotorDriver([pinIN1A, pinIN2A, pinENA], 3, [1, 2])
	## An encoder object
	encoder1 = encoder.Encoder([pyb.Pin.board.PB6, pyb.Pin.board.PB7], 4, [1, 2])
	## A controller object
	controller1 = controller.Controller(K_p=0.10)
	## A motor controller object
	motorcontroller1 = motorcontroller.MotorController(motor, encoder, controller)
	state = 0

	while(True):
		if state == 0:
			# If key is pressed, set state to 1
			if vcp.read() == b'\x31':
				state = 1

			self.controller.clear_data()
			self.controller.set_setpoint(4000)
			self.encoder.zero()
			stop = utime.ticks_add(utime.ticks_ms(), 1000)				


		elif state == 1:
			# Step response
			motorcontroller1.step_response();
			
			# Figure out how and when to set state back to 0
			state = 0


			self.motor.set_duty_cycle(self.controller.run(self.encoder.read()))

		elif state == 2:

		yield (state)


# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.
share0 = task_share.Share ('i', thread_protect = False, name = "Share_0")
motor1_task = cotask.Task(motor1_fun, name = 'Motor 1', priority = 1,
						  period = 1000, profile = True, trace = False)
cotask.task_list.append(motor1_task)




while True:
	cotask.task_list.pri_sched ()

# Print a table of task data and a table of shared information data
print ('\n' + str (cotask.task_list) + '\n')
print (task_share.show_all ())
print (task1.get_trace ())
print ('\r\n')