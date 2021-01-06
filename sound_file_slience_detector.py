import matplotlib.pyplot as plt
import numpy as np
import wave
import sys

#Moving average for smoother curves
#moving_average is an integer
#if moving_averages = 1, then the output is the same dataset as the input
#the more, the smoother the output dataset
#input_data and output_data (return) are both numpy datasets
def get_moving_average(input_data, moving_averages):
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

#exponiential moving average for each
def get_ema_value(input_data, w_decrease, t):
    output_data = np.array([])
    if t = 1:
        return np.array(output_data, input_data[t])

    return np.array(output_data, w_decrease*input_data[t] + (1-w_decrease)*get_ema_value(input_data, w_decrease, t-1))
    

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

moving_averages = 3

smooth_signal = get_moving_average(signal, moving_averages)

print("Finished")

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(time, smooth_signal)
plt.show()


#Now for 1 second per timestep...
