#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 11:48:57 2022

@author: aidan
"""
# Import for searching a directory
import glob
# The GMM Import
from sklearn.mixture import GaussianMixture as GMM
# Import for Gaussian PDF
from scipy.stats import norm
#usual suspects
from ECE16Lib.CircularList import CircularList
import ECE16Lib.DSP as filt
import numpy as np

'''
definitons used in machine learning algorithm
'''
# Retrieve a list of the names of the subjects
def get_subjects(directory):
    filepaths = glob.glob(directory + "/*")
    return [filepath.split("/")[-1] for filepath in filepaths]

# Retrieve a data file, verifying its FS is reasonable
def get_data(directory, subject, trial, fs):
    '''
    print(subject) #uncomment to find faulty data 
    '''
    search_key = "%s/%s/%s_%02d_*.csv" % (directory, subject, subject, trial)
    filepath = glob.glob(search_key)[0]
    t, ppg = np.loadtxt(filepath, delimiter=',', unpack=True)
    t = (t-t[0])/1e3
    hr = get_hr(filepath, len(ppg), fs)
      
    fs_est = estimate_fs(t)
    if(fs_est < fs-1 or fs_est > fs):
        print("Bad data! FS=%.2f. Consider discarding: %s" % (fs_est,filepath))
        
    return t, ppg, hr, fs_est

# Estimate the heart rate from the user-reported peak count
def get_hr(filepath, num_samples, fs):
    count = int(filepath.split("_")[-1].split(".")[0])
    seconds = num_samples / fs
    return count / seconds * 60 # 60s in a minute

# Estimate the sampling rate from the time vector
def estimate_fs(times):
    return 1 / np.mean(np.diff(times))

# Filter the signal (as in the prior lab)
def L7_process(x):
    x = filt.detrend(x, 25)
    x = filt.moving_average(x, 5)
    x = filt.gradient(x)
    return filt.normalize(x)
  



"""
A class to enable a simple heart rate monitor
"""
class HRMonitor:
    """
    Encapsulated class attributes (with default values)
    """
    __hr = 0
    __time = None
    __ppg = None
    __filtered = None  # CircularList containing filtered signal
    __num_samples = 0  # The length of data maintained
    __new_samples = 0  # How many new samples exist to process
    __fs = 0           # Sampling rate in Hz
    __thresh = 0.60     # Threshold from Tutorial 2
    """
    Initialize the class instance
    """
    def __init__(self, num_samples, fs, times=[], data=[]):
      self.__hr = 0
      self.__num_samples = num_samples
      self.__fs = fs
      self.__time = CircularList(data, num_samples)
      self.__ppg = CircularList(data, num_samples)
      self.__filtered = CircularList([], num_samples)
      self.__labels = 0
      
    # Estimate the heart rate given GMM output labels
    def estimate_hr(self, labels, num_samples, fs):
        peaks = np.diff(self.__labels, prepend=0) == 1
        count = sum(peaks)
        seconds = num_samples / fs
        hr = count / seconds * 60 # 60s in a minute
        return hr, peaks
      
      
    """
    Add new samples to the data buffer
    Handles both integers and vectors!
    """
    def add(self, t, x):
      if isinstance(t, np.ndarray):
        t = t.tolist()
      if isinstance(x, np.ndarray):
        x = x.tolist()
        
      if isinstance(x, int):
        self.__new_samples += 1
      else:
        self.__new_samples += len(x)
        
      self.__time.add(t)
      self.__ppg.add(x)
    """
    Compute the average heart rate over the peaks
    """
    def compute_heart_rate(self, peaks):
      t = np.array(self.__time)
      return 60 / np.mean(np.diff(t[peaks]))
    """
    Process the new data to update step count
    """
    def process(self):
      # Grab only the new samples into a NumPy array
      x = np.array(self.__ppg[ -self.__new_samples: ])
      
      # Filter the signal (feel free to customize!)
      x = filt.detrend(x, 25)
      x = filt.detrend(x, 35)
      x = filt.moving_average(x, 5)
      x = filt.moving_average(x, 3)
      x = filt.gradient(x)
      x = filt.normalize(x)
      
      # Store the filtered data
      self.__filtered.add(x.tolist())
      
      # Find the peaks in the filtered data
      count, peaks = filt.count_peaks(self.__filtered, self.__thresh, 1)
      i=0
     
      #remove double counts
      remove_peaks = []
      while (i<len(peaks)-1):
          if len(peaks) > 0:
              if (peaks[i+1] - peaks[i] < 0.2*50):
                  remove_peaks.append(peaks[i])
                  count-=1
          i+=1
    
      peaks = [x for x in peaks if x not in remove_peaks]
    
      # Update the count and reset the new sample count
      self.__hr = self.compute_heart_rate(peaks)
      self.__new_samples = 0
      
      # Return the heart rate, peak locations, and filtered data
      return self.__hr, peaks, np.array(self.__filtered)
    """
    Clear the data buffers and step count
    """
    def reset(self):
      self.__hr = 0
      self.__time.clear()
      self.__ppg.clear()
      self.__filtered.clear()
      
    '''
    When this method is called, it will use ALL of the data in the 
    data folder to train the Gaussian Mixture Model.
    '''
    def train(self):
        print("training...")
        fs = 50
        directory = "./data"
        subjects = get_subjects(directory)
        
        # Leave-One-Subject-Out-Validation
        # 1) Exclude subject
        # 2) Load all other data, process, concatenate
        # 3) Train the GMM
        # 4) Compute the histogram and compare with GMM
        # 5) Test the GMM on excluded subject
        for exclude in subjects:
            print("Training - excluding subject: %s" % exclude)
            train_data = np.array([])
            for subject in subjects:
                for trial in range(1,6):
                    t, ppg, hr, fs_est = get_data(directory, subject, trial, fs)
                    if subject != exclude:
                        train_data = np.append(train_data, L7_process(ppg))
            
            # Train the GMM
            train_data = train_data.reshape(-1,1) # convert from (N,1) to (N,) vector
            gmm = GMM(n_components=2).fit(train_data)
            
            
            # Test the GMM on excluded subject
            print("Testing - all trials of subject: %s" % exclude)
            for trial in range(1,6):
                t, ppg, hr, fs_est = get_data(directory, exclude, trial, fs)
                test_data = L7_process(ppg)
                
                self.__labels = gmm.predict(test_data.reshape(-1,1))
                
                hr_est, peaks = self.estimate_hr(self.__labels, len(ppg), fs)
                print("File: %s_%s: HR: %3.2f, HR_EST: %3.2f" % (exclude,trial,hr,hr_est))
        
    '''
    When the program receives new samples, process them with any filtering
    that you are doing, and then predict the labels using the GMM.
    '''
    def predict(self):
        print("predicting...")
        fs = 50
        # Grab only the new samples into a NumPy array
        x = np.array(self.__ppg[ -self.__new_samples: ])
        print("stage 1")
        # Filter the signal (feel free to customize!)
        x = L7_process(x)
        
        # Store the filtered data
        self.__filtered.add(x.tolist())
        print("stage 2")
        # Find the peaks in the filtered data
        
        self.__hr, peaks = self.estimate_hr(self.__labels, len(x), fs)  #[MACHINE LEARNING CALC GOES HERE]
        print("stage 3")
        # Update the count and reset the new sample count
        self.__new_samples = 0
        print("stage 4")
        self.__hr = self.__hr / 100
        # Return the heart rate, peak locations, and filtered data
        return self.__hr, peaks, np.array(self.__filtered)