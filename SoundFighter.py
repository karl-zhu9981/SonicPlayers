import pyaudio
from KeyPress import *
from matplotlib.mlab import find
import numpy as np
import math
import time
import ctypes

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 100000
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

#Turns raw audio input into frequency data
def Pitch(signal):
	signal = np.fromstring(signal, 'Int16')
#Split Signal by 1/2; Part 1
	signalL = signal[::2]
	crossingL = [math.copysign(1.0, s) for s in signalL]
	indexL = find(np.diff(crossingL));
	f0L = round(len(indexL) * RATE / (2 * np.prod(len(signalL))))

	signalR = signal[1::2]
	crossingR = [math.copysign(1.0, s) for s in signalR]
	indexR = find(np.diff(crossingR));
	f0R = round(len(indexR) * RATE / (2 * np.prod(len(signalR))))

	return [f0L, f0R]


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
	return [strongestFreq, strongestFreq] if frequencies[np.argmax(frequencies)] > 200000 else [0,0]
	#print("The frequency is {} Hz".format(strongestFreq)) if frequencies[np.argmax(frequencies)] > 200000 else print("Noise")


def noteFinder(freq, instrument):
	if ((freq > 946  and freq < 992) or (freq > 482 and freq < 506)):
#	print("b")
		return "b"
	elif ((freq > 860 and freq < 884) or (freq > 429 and freq < 453) or (freq > 1740 and freq < 1790 and instrument==0)):
#	print("a")
		return "a"
	elif ((freq > 774 and freq < 798 ) or (freq > 387 and freq < 405)  or (freq > 1570 and freq < 1595)  ):
#	print("g")
		return "g"
	elif ((freq > 731 and freq < 755) or (freq > 355 and freq < 379)  or (freq > 1460 and freq < 1510) ):
#	print("f#")
		return "f#"
	elif ((freq > 645 and freq < 690) or (freq > 319 and freq < 339) or (freq > 1300 and freq < 1339)):
#	print("e")
		return "e"
	elif ((freq > 555 and freq <604) or (freq > 280 and freq < 304) or(freq > 1740 and freq < 1790 and instrument==1)):
#	print ("Low D")
		return "d"

	elif ((freq > 1141 and freq < 1185)):
#	print ("Low D")
		return "d"
	elif ((freq > 510 and freq < 540)):
#	print ("Low D")
		return "c"
	else:
#		print("Frequency: ", freq)
		return None

currentNote = ["",""]
noteCounter = [0,0]

def movKeyPress(Frequency):
	sleep = False
	noteChanged = False
	for i in range(0, 2):
		note = noteFinder(Frequency[i],i)
		if (note != None):
			print(note)
			if (note == currentNote[i]):
				if (note == "b"):
					if(i==0):
						PressKey(DIK_Z)
					else:
						PressKey(DIK_Q)
					sleep = True
				elif (note == "a"):
					if(i==0):
						PressKey(DIK_X)
					else:
						PressKey(DIK_E)
					sleep = True
				elif (note == "g"):
					if(i==0):
						PressKey(DIK_W)
					else:
						PressKey(DIK_I)
					sleep = True
				elif (note == "f#"):
					if (i == 0):
						PressKey(DIK_S)
					else:
						PressKey(DIK_K)
					sleep = True
				elif (note == "e"):
					if(i==0):
						PressKey(DIK_D)
					else:
						PressKey(DIK_L)
					sleep = True
				elif (note == "d"):
					if (i == 0):
						PressKey(DIK_A)
					else:
						PressKey(DIK_J)
					sleep = True
				elif (note == "c"):
					if (i == 0):
						PressKey(DIK_R)
					else:
						PressKey(DIK_C)
					sleep = True
			elif (note != currentNote[i]):
				noteChanged = True
				noteCounter[i] = 0
			currentNote[i] = note
			noteCounter[i] += 1
		else:
			#print("Frequency: ", Frequency[i])
			noteChanged = True
			noteCounter[i] = 0
			currentNote[i] = ""
	return noteChanged

def movKeyPressRel(Freq):
	if(movKeyPress(Freq)):
		#time.sleep(0.1)
		ReleaseKey(DIK_I)
		ReleaseKey(DIK_J)
		ReleaseKey(DIK_K)
		ReleaseKey(DIK_L)
		ReleaseKey(DIK_Z)
		ReleaseKey(DIK_X)
		ReleaseKey(DIK_Q)
		ReleaseKey(DIK_E)
		ReleaseKey(DIK_W)
		ReleaseKey(DIK_S)
		ReleaseKey(DIK_D)
		ReleaseKey(DIK_A)
		ReleaseKey(DIK_C)
		ReleaseKey(DIK_R)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
					rate=RATE, input=True,
					frames_per_buffer=CHUNK)
frames = []
frequencies = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# Takes data from stream over duration of 1024 frames(Chunk Size)
	data = stream.read(CHUNK)
# Adds Data to frame for save to .wav file
	frames.append(data)
# Adds Data to frame for save to Frequency file
	freq=FFTPitch(data)
	movKeyPressRel(freq)
	frequencies.append(freq)
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
