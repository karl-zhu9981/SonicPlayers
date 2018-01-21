import pyaudio
from KeyPress import *
from matplotlib.mlab import find
import numpy as np
import math
import time

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1000
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

'''Notes for D major scale D5 lowest note'''
notes = {947:"b",969:"b",991:"b",
		883:"a", 861:"a",
		775:"g",797:"g",
		732:"f#",754:"f#",
		646:"e",668:"e",689:"e",
		581:"Low D", 560:"Low D", 603:"Low D"}

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

	return [f0L, f0R];


def noteFinder(freq):
	if (freq > 946  and freq < 992) or (freq > 482 and freq < 506):
#	print("b")
		return "b"
	elif ((freq > 860 and freq < 884) or (freq > 429 and freq < 453)):
#	print("a")
		return "a"
	elif ((freq > 774 and freq < 798 )or (freq > 387 and freq < 405) ):
#	print("g")
		return "g"
	elif ((freq > 731 and freq < 755) or (freq > 355 and freq < 379) ):
#	print("f#")
		return "f#"
	elif ((freq > 645 and freq < 690)or (freq > 319 and freq < 339)):
#	print("e")
		return "e"
	elif ((freq > 555 and freq <604)or (freq > 280 and freq < 304)):
#	print ("Low D")
		return "Low D"

	elif ((freq > 1141 and freq < 1184) ):
#	print ("Low D")
		return "d"
	else:
#		print("Frequency: ", freq)
		return None

currentNote = ["",""]
noteCounter = [0,0]
'''VK KEYS'''
def movVkKeyPress(Frequency):
	sleep = False
	for i in range(0, 2):
		if (noteFinder(Frequency[i])!= None):
			note = noteFinder(Frequency[i])
			print(note)
			if (note == currentNote[i] and noteCounter[i] >= 2):
				if (note == "b"):
					if(i==0):
						PressKey(KEY_X)
					else:
						PressKey(KEY_Q)
					sleep = True
				elif (note == "a"):
					if(i==0):
						PressKey(KEY_Z)
					else:
						PressKey(KEY_E)
					sleep = True
				elif (note == "g"):
					if(i==0):
						PressKey(KEY_W)
					else:
						PressKey(KEY_I)
					sleep = True
				elif (note == "f#"):
					if (i == 0):
						PressKey(KEY_S)
					else:
						PressKey(KEY_K)
					sleep = True
				elif (note == "e"):
					if(i==0):
						PressKey(KEY_D)
					else:
						PressKey(KEY_L)
					sleep = True
				elif (note == "Low D"):
					if (i == 0):
						PressKey(KEY_A)
					else:
						PressKey(KEY_J)
					sleep = True
			elif (note != currentNote[i]):
				noteCounter[i] = 0
			currentNote[i] = note
			noteCounter[i] += 1
		else:
			print("Frequency: ", Frequency[i])
			noteCounter[i] = 0
			currentNote[i] = ""
	return sleep

def movVkKeyPressRel(Freq):
	if(movVkKeyPress(Freq)):
		time.sleep(0.1)
		ReleaseKey(KEY_I)
		ReleaseKey(KEY_J)
		ReleaseKey(KEY_K)
		ReleaseKey(KEY_L)
		ReleaseKey(KEY_Z)
		ReleaseKey(KEY_X)
		ReleaseKey(KEY_Q)
		ReleaseKey(KEY_E)
		ReleaseKey(KEY_W)
		ReleaseKey(KEY_S)
		ReleaseKey(KEY_D)
		ReleaseKey(KEY_A)
'''DirectX Key map'''
def movDicKeyPress(Frequency):
	sleep = False
	print(Frequency)
	for i in range(0,2):
		if (noteFinder(Frequency[i])!=None):
			note = noteFinder(Frequency[i])
			print(note)
			if (note == currentNote[i] and noteCounter[i] > 2):
				if (note == "b"):
					if(i==0):
						PressKey(DIK_X)
					else:
						PressKey(DIK_Q)
					sleep = True
				elif (note == "a"):
					if(i==0):
						PressKey(DIK_Z)
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
				elif (note == "Low D"):
					if (i == 0):
						PressKey(DIK_A)
					else:
						PressKey(DIK_J)
					sleep = True
			if (note != currentNote[i]):
				noteCounter[i] = 0
			currentNote[i] = note
			noteCounter[i] += 1
		else:
			print("Frequency: ", Frequency[i])
	return sleep

def movDicKeyPressRel(Freq):
	if(movDicKeyPress(Freq)):
		time.sleep(0.1)
		ReleaseKey(DIK_W)
		ReleaseKey(DIK_S)
		ReleaseKey(DIK_A)
		ReleaseKey(DIK_D)
		ReleaseKey(DIK_Z)
		ReleaseKey(DIK_X)
		ReleaseKey(DIK_Q)
		ReleaseKey(DIK_E)
		ReleaseKey(DIK_I)
		ReleaseKey(DIK_K)
		ReleaseKey(DIK_L)
		ReleaseKey(DIK_J)


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
	freq=Pitch(data)
	movVkKeyPressRel(freq)
	frequencies.append(freq)
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
