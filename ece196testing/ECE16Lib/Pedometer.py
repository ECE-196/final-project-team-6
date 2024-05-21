#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Oct 25 17:10:12 2022
@author: aidan
"""

from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

"""
A class to enable a simple step counter
"""
class Pedometer:
    """
    Encapsulated class attributes (with default values)
    """
    __steps = 0        # the current step count
    __l1 = None        # CircularList containing L1-norm
    __filtered = None  # CircularList containing filtered signal
    __num_samples = 0  # The length of data maintained
    __new_samples = 0  # How many new samples exist to process
    __fs = 0           # Sampling rate in Hz
    __b = None         # Low-pass coefficients
    __a = None         # Low-pass coefficients
    __thresh_low = 15  # Threshold from Tutorial 2
    __thresh_high = 70# Threshold from Tutorial 2
    __jump_low = 70  # Threshold for jump
    __jump_high = 150# Threshold for jump
    
    """
    Initialize the class instance
    """
    def __init__(self, num_samples, fs, data=None):
        self.__steps = 0
        self.__jumps = 0
        self.__num_samples = num_samples
        self.__fs = fs
        self.__l1 = CircularList(data, num_samples)
        self.__filtered = CircularList([], num_samples)
        self.__b, self.__a = filt.create_filter(3, 1, "lowpass", fs)
    """
    Add new samples to the data buffer
    Handles both integers and vectors!
    """
    def add(self, ax, ay, az):
        l1 = filt.l1_norm(ax, ay, az)
        if isinstance(ax, int):
            num_add = 1
        else:
            num_add = len(ax)
            l1 = l1.tolist()
            
        self.__l1.add(l1)
        self.__new_samples += num_add
    """
    Process the new data to update step count
    """
    def process(self):
        # Grab only the new samples into a NumPy array
        x = np.array(self.__l1[ -self.__new_samples: ])
        
        # Filter the signal (detrend, LP, MA, etc...) # ...
        
        bl, al = filt.create_filter(3, 1, "lowpass", self.__fs)# Low-pass Filter Design
        F = filt.filter(bl, al, x)  # Low-pass Filter Signal
        
        dt = filt.detrend(F)# Detrend the Signal
        
        ma = filt.moving_average(dt, 20)# Compute Moving Average

        #grad = filt.gradient(ma)# Compute the Gradient
        #freqs, power = filt.psd(az, len(az), 50)# Power Spectral Density

        
        # Store the filtered data
        self.__filtered.add(ma.tolist())
        
        # Count the number of peaks in the filtered data
        ama = np.abs(ma)
        count, peaks = filt.count_peaks(ama,self.__thresh_low,self.__thresh_high)
        self.__steps += count
        
        count, peaks = filt.count_peaks(ama,self.__jump_low,self.__jump_high)
        self.__jumps += count
        
        self.__new_samples = 0
        # Return the step count, peak locations, and filtered data
        return self.__steps, self.__jumps, peaks, np.array(self.__filtered), 


    """
    jump counter
    """

    
    """
    Clear the data buffers and step count
    """
    def reset(self):
        self.__steps = 0
        self.__l1.clear()
        self.__filtered = np.zeros(self.__num_samples)