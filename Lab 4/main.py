## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date February 14, 2019

import pyb
import micropython
import gc

import utime

import motor
import encoder
import controller

import cotask
import task_share
import print_task



# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf(100)

# Set up pin C0 as an input pin
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.IN)
# Set up pin C1 as an output pin
pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)

# Set up Timer 1 to create interrupts at 1 KHz
timer = pyb.Timer(1, freq=1000)

# Set up ADC to read pin C0
adcPC0 = pyb.ADC(pyb.Pin.board.PC0)

# Set up time quene
time = task_share.Queue('I', 1000, thread_protect = True, overwrite = False,
						   name = 'Time')
# Set up values quene
vals = task_share.Queue('I', 1000, thread_protect = True, overwrite = False,
						   name = 'Values')

# Define a function that reads ADC on pin C0
def read_adcPC0(timer):
	time.put(utime.ticks_ms())
	vals.put(adcPC0.read())



# MAIN PROGRAM

# Activate interrupt callback
pinC1.low()
timer.callback(read_adcPC0)
utime.sleep_ms(100)

# Step input
pinC1.high()
utime.sleep_ms(900)

# Deactivate interrupt callback
timer.callback(None)
pinC1.low()

# Print from quene
t_0 = time.get()
print('0, ' + str(vals.get()))
while vals.any():
	print(str(int(time.get())-t_0) + ', ' + str(vals.get()))



# =============================================================================

# Create the tasks. If trace is enabled for any task, memory will be allocated
# for state transition tracing, and the application will run out of memory
# after a while and quit. Therefore, use tracing only for debugging and set
# trace to False when it's not needed.



# # Create inter-task communication variables
# pos_ctrl1 = task_share.Share('H', thread_protect=False, name='Position Control 1')
# setpoint1 = task_share.Share('I', thread_protect=False, name='Setpoint 1')
# step_rsp1 = task_share.Share('H', thread_protect=False, name='Step Response 1')
# get_data1 = task_share.Share('H', thread_protect=False, name='Get Data 1')
# pos_ctrl2 = task_share.Share('H', thread_protect=False, name='Position Control 2')
# setpoint2 = task_share.Share('I', thread_protect=False, name='Setpoint 2')
# step_rsp2 = task_share.Share('H', thread_protect=False, name='Step Response 2')
# get_data2 = task_share.Share('H', thread_protect=False, name='Get Data 2')



# # Create tasks
# motor1_task = cotask.Task(motor1_fun, name='Motor 1', priority=2,
# 						  period=10, profile=True, trace=False)
# cotask.task_list.append(motor1_task)
# motor2_task = cotask.Task(motor2_fun, name='Motor 2', priority=2,
# 						  period=10, profile=True, trace=False)
# cotask.task_list.append(motor2_task)
# # user_input = cotask.Task(user_input, name='Motor 1', priority=1,
# # 						  period=750, profile=True, trace=False)
# # cotask.task_list.append(user_input)
# manual_control = cotask.Task(manual_control, name='Manual Control', priority=1,
# 						  period=10, profile=True, trace=False)
# cotask.task_list.append(manual_control)



# # Run the memory garbage collector to ensure memory is as defragmented as
# # possible before the real-time scheduler is started
# gc.collect()

# # Run the scheduler with the chosen scheduling algorithm. Quit if any 
# # character is sent through the serial por
# vcp = pyb.USB_VCP()
# while not vcp.any():
# 	cotask.task_list.pri_sched()

# # Empty the comm port buffer of the character(s) just pressed
# vcp.read()

# # Print a table of task data and a table of shared information data
# print('\n' + str (cotask.task_list) + '\n')
# print(task_share.show_all ())
# # print the motor2_task as well
# print(motor1_task.get_trace ())
# print('\r\n')