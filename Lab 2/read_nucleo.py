## @file main.py
#  TODO
#
#  @author Rahul Goyal, Cameron Kao, Harry Whinnery
#
#  @copyright License Info
#
#  @date January 31, 2019

import serial


port = 'COM4'



with serial.Serial(port) as rahul:
    # Ctrl + C
    rahul.write(b'\x03')
    # Ctrl + D
    rahul.write(b'\x04')
    # Carriage Return
    rahul.write(b'\x0D')



    print(rahul.read(100))