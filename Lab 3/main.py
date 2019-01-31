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

import cotask
import task_share
import print_task
import busy_task

# Allocate memory so that exceptions raised in interrupt service routines can
# generate useful diagnostic printouts
micropython.alloc_emergency_exception_buf (100)



# =============================================================================

if __name__ == "__main__":
	pass