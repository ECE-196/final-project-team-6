#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:13:14 2024

@author: aidan
"""

# importing the pygame library 
import pygame 
import pygame.camera 
import time
import serial
#from serial import Serial
#from ECE16Lib.Communication import Communication
# import json

#comms.clear() # just in case any junk is in the pipes

  
# initializing  the camera 
pygame.camera.init()
  
# make the list of all available cameras 
camlist = pygame.camera.list_cameras() 
  
# if camera is detected or not 
if camlist: 
  
    # initializing the cam variable with default camera 
    cam = pygame.camera.Camera(camlist[0], (960, 960), "RGB") 
    num = 0
    # opening the camera 
    cam.start() 
  
    # capturing the single image
    print("Camera started") 
    
    while (num < 10):
        image = cam.get_image() 
        brighten = 40
        image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)
        
        # saving the image to SAME FOLDER as code
        pygame.image.save(image, "pic%s.jpg" % num) 
        
        # run analysis here to output letter
        #
        # 
        #
        #
        
        
        #SEND found value to arduino
        ser = serial.Serial('/dev/cu.usbmodem14401')  # open serial port
        print(ser.name)         # check which port was really used
        ser.write(b'a')     # write a string
        ser.close()
        
        #wait between photos
        num = num + 1
        time.sleep(1)
    
    print("%s photos taken" % num) 
    
  
# if camera is not detected the moving to else part 
else: 
    print("No camera on current device") 