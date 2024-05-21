from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
import time
import numpy as np
import cv2



#plot style
plt.style.use('seaborn-whitegrid')

#get the epoch
obj = time.gmtime(0)
epoch = time.asctime(obj)

#Sampling Settings
fs = 50                         # sampling rate
num_samples = 250               # 5 seconds of data @ 50Hz
process_time = 5                # compute the hr count every second

#initialize arrays
ppg = []
timestamps = []
#initialize camera, heart rate class
cap = cv2.VideoCapture(0) # choose your appropriate camera!
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) ==> use this instead if you’re on Windows!

heart = HRMonitor(num_samples, fs, [])


if __name__ == "__main__":
    #Start heart rate monitor

    input("Ready to collect data? Press [ENTER] to begin.\n")
    print("Start measuring in...")
    '''
    for k in range(3,0,-1):
        print(k)
        time.sleep(1)
    print("Begin!")
    '''

    try:
        previous_time = time.time()
        #Sampling and calculations

        while(True):

            _, frame = cap.read()
            new_sample = frame.mean(axis=0).mean(axis=0)
            new_sample = new_sample[2] # replace the ? with index of the RED channel
            ppg.append(new_sample) # append new_sample to ppg
            timestamps.append(time.time_ns())

            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c == 27:
                break
            # if enough time has elapsed, process the data and plot it
            current_time = time.time()
            if (current_time - previous_time > process_time):
                previous_time = current_time
                t = np.array(timestamps[10:]) # so we can easily subtract the first time
                t = t - t[0]
                t = t/1E9
                p = ppg[10:] # remove the first few points because of auto-exposure
                heart.add(t,p)
                try:
                    hr, peaks, filtered = heart.process()
                except:
                    continue

                #if HR monitor is finding 0 peaks, check to catch it so that infinite heart rate isn't reported

                if peaks == 0:
                    hr = 0
                else:
                    print("heart rate: {:.2f}".format(hr))

                fig = plt.figure()
                ax = plt.axes()

                plt.cla()
                
                plt.xlabel("time(s)")
                plt.ylabel("Red Channel Value")

                #ax.plot(t, p)
                plt.plot(filtered)
                plt.title("heart rate: {:.2f}".format(hr))
                plt.show(block=False)
               
                plt.pause(0.001)

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
                
        cap.release()
        cv2.destroyAllWindows()


