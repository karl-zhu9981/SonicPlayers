import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from matplotlib.mlab import find

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 100000
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

def FFTPitch(signal):
	# convert the raw data into a usable format
	data = np.fromstring(signal, 'Int16')
	# toss it in a numpy array
	data = np.array(data)
	# apply a fast fourier transformation to the data
	# This converts it into an array of frequency amplitudes
	data_fft = np.fft.fft(data)
	# FFT gives complex numbers, so remove those so it's all real
	frequencies = np.abs(data_fft)
	# Filter out the noise
	frequencies = [f if (1 < index < 50 and f > 1) else 0 for index, f in enumerate(frequencies)]
	
	strongestFreq = np.argmax(frequencies)*RATE/CHUNK
	print("The frequency is {} Hz".format(strongestFreq)) if frequencies[np.argmax(frequencies)] > 200000 else print("Noise")
	#print(frequencies[np.argmax(frequencies)])
	#print(Pitch(signal))

	plt.draw()
	plt.clf()
	plt.subplot(2,1,1)
	plt.title("Original audio wave")
	plt.plot(data[:300])
	plt.subplot(2,1,2)
	plt.title("Frequencies found")
	plt.xlim(0,50)
	plt.plot(frequencies)
	plt.pause(0.00001)

def Pitch(signal):
	signal = np.fromstring(signal, 'Int16')
#Split Signal by 1/2; Part 1
	signalL = signal#[::2]
	crossingL = [math.copysign(1.0, s) for s in signalL]
	indexL = find(np.diff(crossingL));
	f0L = round(len(indexL) * RATE / (2 * np.prod(len(signalL))))

	signalR = signal[1::2]
	crossingR = [math.copysign(1.0, s) for s in signalR]
	indexR = find(np.diff(crossingR));
	f0R = round(len(indexR) * RATE / (2 * np.prod(len(signalR))))

	return [f0L, f0R]

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)
frames = []
frequencies = []
plt.show()
plt.subplot(2,1,1)
plt.title("Original audio wave")
plt.subplot(2,1,2)
plt.title("Frequencies found")
plt.xlim(0,50)
plt.ylim(0,150000000)

plt.ion()
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# Takes data from stream over duration of 1024 frames(Chunk Size)
	#time.sleep(3)

	data = stream.read(CHUNK)
# Adds Data to frame for save to .wav file
	frames.append(data)
# Adds Data to frame for save to Frequency file
	freq=FFTPitch(data)
	#movKeyPressRel(freq)
	frequencies.append(freq)
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
