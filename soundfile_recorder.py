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
RECORD_SECONDS = 500
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
unique = []
dictionary = {}
#---------------

dictionary =  {1184.0: "Low D", 1206.0: "Low D", 668.0: "E", 646.0: "E",732.0: "F#", 754.0:"F#",775.0: "G", 797.0: "G", 883.0: "A", 861.0:"A",969.0: "B", 
991.0: "B" , 1141.0: "C", 1120.0: "C", 1098.0: "C", 1184.0:"High D"}

#---------------
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    Frequency=Pitch(data)

    
    print ("Frequency: ",Frequency)
    if Frequency in dictionary:
        print(dictionary[Frequency])
        if dictionary[Frequency] == "A":
            pyautogui.press('left')
        if dictionary[Frequency] == "G":
            pyautogui.press('right')








