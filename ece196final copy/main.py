#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 09:09:45 2022

@author: aidan
"""

import serial # the PySerial library
import time # for timing purposes

def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

def close(ser):
    ser.close()

def receive_message(ser, num_bytes=50):
    if(ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None
    
def send_message(ser, message):
   if(message[-1] != '\n'):
       message = message + '\n'
   ser.write(message.encode('utf-8'))
   
def main():
    ser = setup("/dev/cu.AidanBT", 115200)
    send_message(ser, " ")
    time.sleep(3)
    message = None
    i = 0
    
    while message == None:
        test = "Arduino test case #1"
        sendable = test[i]
        
        send_message(ser, sendable)
        time.sleep(1)
    
        
        if i > len(test):
            message = receive_message(ser)
        i = i + 1
        
    print("done")
    close(ser)
    
    
    
"""
Main entrypoint for the application
"""
if __name__== "__main__":
    main()
