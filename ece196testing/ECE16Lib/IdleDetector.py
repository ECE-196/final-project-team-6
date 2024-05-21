#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 21:36:25 2022

@author: aidan
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

class CircularList(list):
    
    def __init__(self, data, maxlen=0):
        assert isinstance(data, list), "Invalid data. It must be a list."
        comms = Communication("/dev/cu.AidanBT", 115200)
        num_samples = 250 # 5 seconds of data @ 50Hz 
          
        times = CircularList([], num_samples)
        ax = CircularList([], num_samples)
        ay = CircularList([], num_samples)
        az = CircularList([], num_samples)
        L2 = CircularList([], num_samples)
        
        comms.send_message("idle") # begin sending data
            # initialize the parent list constructor with the data
        super().__init__(data)
    
    def check(self, data):
        try:
          previous_time = 0
          while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError: # if corrupted data, skip the sample 
                    continue
                
                # add the new values to the circular lists
                times.add(int(m1))
                ax.add(int(m2))
                ay.add(int(m3))
                az.add(int(m4))
                norm2 = ax[-1]**2 + ay[-1]**2 + az[-1]**2
                norm2 = np.sqrt(norm2)
                L2.add(norm2)
              
                if np.max(L2) > 3600: #check last 5 seconds of data for activity
                    self = True
                else:
                    self = False
