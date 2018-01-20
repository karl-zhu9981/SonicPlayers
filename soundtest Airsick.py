from matplotlib.mlab import find
import pyaudio
import numpy as np
import pyautogui
import math
import keyboard


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 1000


def Pitch(signal):
	signal = np.fromstring(signal, 'Int16');
	crossing = [math.copysign(1.0, s) for s in signal]
	index = find(np.diff(crossing));
	f0=round(len(index) *RATE /(2*np.prod(len(signal))))
	return f0;


p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
channels = CHANNELS,
rate = RATE,
input = True,
output = True,
frames_per_buffer = chunk)

for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
	data = stream.read(chunk)
	Frequency=Pitch(data)
	if(Frequency>2900 and Frequency<3000):
		print("b")
	elif(Frequency == 2627 or Frequency == 2606 or Frequency == 2649 or Frequency == 2584):
		print("a")
		#pyautogui.keyDown('left')
		#keyboard.release('left')
		pyautogui.press('left')
	elif(Frequency == 2326 or Frequency == 2304 or Frequency == 2347 or Frequency == 2369):
		print("g")
		#keyboard.press_and_release('right')
		pyautogui.press('right')
	elif(Frequency == 2218 or Frequency == 2196 or Frequency == 2261):
		print("f#")
	elif(Frequency == 646 or Frequency == 668 or Frequency == 689):
		print("e")
	elif(Frequency==581 or Frequency == 560 or Frequency == 603):
		print("Low D")
	else:
		print ("Frequency: ",Frequency)
	#notes = {2627:'a',2606:'a',2649:'a',2326:'b'}
	#note = notes[Frequency]