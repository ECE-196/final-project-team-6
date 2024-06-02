#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 12:12:11 2022

@author: aidan
"""

from ECE16Lib.Communication import Communication
from time import sleep

if __name__ == "__main__":

    #comms connections
    comms = Communication("/dev/cu.usbserial-0230F2AC", 115200)
    comms.clear() # just in case any junk is in the pipes
      
    comms.send_message("Connected") #send connected message to confirm for both
    sleep(2)
    End = False
  
    try:
        while(End == False):
            test_message = "12345"
            comms.send_message(test_message)
            print("message 1")
            sleep(2)

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()
