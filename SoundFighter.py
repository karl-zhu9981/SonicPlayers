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
	return strongestFreq if frequencies[np.argmax(frequencies)] > 200000 else -1
	#print("The frequency is {} Hz".format(strongestFreq)) if frequencies[np.argmax(frequencies)] > 200000 else print("Noise")

def getPitches(signal, instruments):
	Frequencys = []
	for i in range(0,instruments):
		Frequencys.append(FFTPitch(signal[i::instruments]))
	return Frequencys

def getNote(freq):
	return {
		-99999<freq<99999:None,
		280<freq<304:"d",
		319<freq<339:"e",
		355<freq<379:"f#",
		387<freq<405:"g",
		429<freq<453:"a",
		482<freq<506:"b",
		510<freq<540:"c",
		555<freq<604:"d",
		645<freq<690:"e",
		731<freq<755:"f#",
		774<freq<798:"g",
		860<freq<884:"a",
		946<freq<992:"b",
		1141<freq<1185:"d",
		1300<freq<1339:"e",
		1460<freq<1510:"f#",
		1570<freq<1595:"g",
		1740<freq<1790:"a"
	}[1]

currentNote = ["",""]
noteCounter = [0,0]
keyMappings = [{"c":DIK_C,"d":DIK_A, "e":DIK_D, "f#":DIK_S, "g":DIK_W, "a":DIK_X, "b":DIK_Z},
			   {"c":DIK_R,"d":DIK_J, "e":DIK_L, "f#":DIK_K, "g":DIK_I, "a":DIK_E, "b":DIK_Q}]

# presses down keys corresponding to the notes currently being played
# then returns a list of notes to be released
def movKeyPress(Frequency):
	note = []
	notesToRelease = []
	for i in range(0, len(Frequency)):
		note.append(getNote(Frequency[i]))
		if (note[i] != None):
			print(note)
			PressKey(keyMappings[i][note[i]])
			if (note[i] != currentNote[i]):
				notesToRelease.append(currentNote[i])
			currentNote[i] = note[i]
			noteCounter[i] += 1
		else:
			#print("Frequency: ", Frequency[i])
			notesToRelease.append(currentNote[i])
			noteCounter[i] = 0
			currentNote[i] = ""
	return notesToRelease

def movKeyPressRel(Freq):
	notesToRelease = movKeyPress(Freq)
	for i in range(0,len(notesToRelease)):
		if(notesToRelease[i]!=''):
			ReleaseKey(keyMappings[i][notesToRelease[i]])


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
	freq = getPitches(data, CHANNELS)
	movKeyPressRel(freq)
	frequencies.append(freq)
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
