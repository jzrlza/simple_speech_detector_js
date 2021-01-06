import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#path of the audio file
audio_data = wave.open("test_voice.wav", "r")

signal = audio_data.readframes(-1)
signal = np.fromstring(signal, "Int16")
fs = audio_data.getframerate()

# If Stereo
if audio_data.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

signal_steps = len(signal)


time = np.linspace(0, signal_steps / fs, num=signal_steps)

time_steps = len(time)

print("Signals : "+str(signal_steps))
print(signal)
print("Time : "+str(time_steps))
print(time)

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(time, signal)
plt.show()


#Now for 1 second per timestep...
