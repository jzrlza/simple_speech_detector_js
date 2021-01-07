import numpy as np
import matplotlib.pyplot as plt
import wave
import sys
import math

#####Functions#####

def sma(data, t):
    print("dd")

def ema(data, t, i):
    if i == 0:
        return sma(data,t, start, end)
    k = 2/(t+1)
    ema = data[i]*k + (1-k)*data[i-1]
    return ema
    #n = end_point + 1 - start_point
    #for timestep in range(start_point, end_point+1):
    #    print("dd")
    #    if timestep == 0:

def get_sd(data, mean, start, end):
    summation = 0.0
    n = end - start + 1
    for i in range(start,end+1):
        summation = (data[i]-mean)**2
    return math.sqrt(summation/n)

##INPUT##
audio_data = wave.open("test_voice.wav", "r")

signal = audio_data.readframes(-1)
signal = np.fromstring(signal, "Int16")
fs = audio_data.getframerate()

#If Stereo, exit, unsupported.
if audio_data.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

time = np.linspace(0, len(signal) / fs, num=len(signal))
time = time.tolist()
##Threshold settings##
voice_sd_threshold = 160
steps_threshold = 20

#Values
timestamp_of_recent_silence = {}
timestamp_of_recent_silence_lst = []
summation = 0.0
average_chunk = 0.0
prev_sd = 0.0
start = 0

####Loop through Time####
for timestamp in range(len(signal)):
    print("%d of %d timestep" % (timestamp, len(signal)-1))
    summation += signal[timestamp]
    #print(signal[timestamp])
    
    if (timestamp+1) % steps_threshold == 0:
        #print("SUM "+str(average_chunk))
        average_chunk = summation / steps_threshold
        #print("AVG "+str(average_chunk))
        #mean = ema(data, t, i)

        sd = get_sd(signal,average_chunk,start,timestamp)
        #print("SD "+str(sd))

        if sd - prev_sd > voice_sd_threshold :
            #print("LOUD!!")
            timestamp_of_recent_silence.update({timestamp:"at_this_timestep_the_silience_ended"})
            timestamp_of_recent_silence_lst.append(timestamp)
            
        average_chunk = 0.0
        start = timestamp+1
        prev_sd = sd
        sd = 0.0
        
###OUTPUT###
with open("output_timestamps.json","w", encoding="utf-8") as jsonfile:
    json.dump(timestamp_of_recent_silence, jsonfile, ensure_ascii=False, indent=2)

##VISUALIZE##
plt.figure(1)
plt.title("Signal Wave...")

plt.plot(time, signal, label="sound")
plt.plot(time, signal, markevery=timestamp_of_recent_silence_lst, ls="", marker="o", label="points")
plt.show()

