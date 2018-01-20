from matplotlib.mlab import find
import pyaudio
import numpy as np
import math

chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 20


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

def getFrequency():
    frequencies= []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        Frequency=Pitch(data)
        frequencies.append(Frequency)
    desiredFrequency=max(frequencies)-min(frequencies)
    return desiredFrequency
    
def getNote():
    if getFrequency()>2900 and getFrequency()<3000:
        pyautogui.press('up')
        print("b")
    if getFrequency() == 2627 or getFrequency() == 2606 or getFrequency() == 2649 or getFrequency() == 2584:
    	pyautogui.press('down')
    	print("a")
    if getFrequency() == 2326 or getFrequency() == 2304 or getFrequency() == 2347 or getFrequency() == 2369:
    	pyautogui.press('left')
    	print("g")
    elif getFrequency()==581 or getFrequency() == 560 or getFrequency() == 603:
        pyautogui.press('right')
    	print("Low D")
    else:
    	print ("Frequency: ",Frequency)

getNote()
