import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#Moving average for smoother curves
#moving_average is an integer
#if moving_averages = 1, then the output is the same dataset as the input
#the more, the smoother the output dataset
#input_data and output_data (return) are both numpy datasets
def moving_average(moving_averages, input_data):
    output_data = np.array([])
    for j in range(len(input_data) - 1) :
        print("%d of %d" % (j, len(input_data)))
        x = 0.0
        print(f"%d to %d" % (j,j+moving_averages-1))
        for i in range(j,j+moving_averages):
            x_before = x
            x += input_data[i]
            print(f"%d : (%.2f)+(%.2f) = %.2f" % (i, x_before, input_data[i], x))

        print(f"Summed : %.2f" % (x))
        x = x / float(moving_averages)
        print(f"Averaged : %.2f" % (x))

        output_data = np.append(output_data, x)
        print("Result")
        print(output_data)

    return output_data

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
total_time_of_sound_in_seconds = time[len(time)-1]
time_steps_per_second = time_steps / total_time_of_sound_in_seconds

print("Signals : "+str(signal_steps)+" steps")
print(signal)
print("Time : "+str(time_steps)+" steps")
print(time)
print("Timesteps per sec : "+str(time_steps_per_second))

#Moving average for smoother curves
#if = 1, then it is the same set
#the more, the smoother
moving_averages = 3

smooth_signal = moving_average(moving_averages, signal)

print("Finished")

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(time, smooth_signal)
plt.show()


#Now for 1 second per timestep...
