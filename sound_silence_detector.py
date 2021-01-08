import numpy as np
import matplotlib.pyplot as plt
import wave
import sys
import math
import json

#####Functions#####

#Get Standard Deviation (rate of value change in a data chunk)
#data => numpy or list of numbers (np, list)
#mean => calculated mean of the data, this to avoid looping again (float)
#start => start index of the data (int)
#end => end index of the data, matches the last one (int)
def get_sd(data, mean, start, end):
    summation = 0.0
    n = end - start + 1
    for i in range(start,end+1):
        summation = (data[i]-mean)**2
    return math.sqrt(summation/n)

##INPUT##
audio_data = wave.open("test_voice_real.wav", "r")

signal = audio_data.readframes(-1)
signal = np.fromstring(signal, "Int16")
fs = audio_data.getframerate()

#If Stereo, exit, unsupported.
if audio_data.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

#Time list
time = np.linspace(0, len(signal) / fs, num=len(signal))
time = time.tolist()

####Threshold settings####
voice_sd_threshold = 480
steps_threshold = 201

###Values###
timestamp_of_recent_silence = {}
timestamp_of_loud_or_not = []
is_loud = False
summation = 0.0
average_chunk = 0.0
prev_sd = 0.0
start = 0

####Loop through Time####
for timestamp in range(len(signal)):
    #Print progress, as this may take time
    print("%d of %d timestep" % (timestamp, len(signal)-1))
    
    #Do a summation, so we are able to loop just once for better runtime.
    summation += signal[timestamp]

    #Finish a chunk
    if (timestamp+1) % steps_threshold == 0:
        average_chunk = summation / steps_threshold

        sd = get_sd(signal,average_chunk,start,timestamp)

        #Loud check
        if sd - prev_sd > voice_sd_threshold :
            seconds = f"%.2f seconds" % (time[timestamp])
            timestamp_of_recent_silence.update({timestamp:seconds})
            is_loud = True
        else:
            is_loud = False

        #reset and go to next chunk
        average_chunk = 0.0
        start = timestamp+1
        prev_sd = sd
        sd = 0.0

    timestamp_of_loud_or_not.append(is_loud)
        
###OUTPUT###
with open("output_timestamps.json","w", encoding="utf-8") as jsonfile:
    json.dump(timestamp_of_recent_silence, jsonfile, ensure_ascii=False, indent=2)

##VISUALIZE##
plt.figure(1)
plt.title("Signal Wave...")

fig, ax = plt.subplots()

ax.plot(time, signal, label="sound")
ax.fill_between(time, 0,1, color='#539ecd', where=timestamp_of_loud_or_not, transform=ax.get_xaxis_transform())

plt.show()

