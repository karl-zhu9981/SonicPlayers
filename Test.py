import pyautogui
import pyaudio
import wave
import sys
from matplotlib.mlab import find
import numpy as np
import math

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 512
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()


#Turns raw audio input into frequency data
def Pitch(signal):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;

def noteFinder(freq):
    if(Frequency == 2627 or Frequency == 2606 or Frequency == 2649 or Frequency == 2584):
    	pyautogui.press('down')
    	print("a")
    if(Frequency == 2326 or Frequency == 2304 or Frequency == 2347 or Frequency == 2369):
    	pyautogui.press('left')
    	print("g")
    elif(Frequency==581 or Frequency == 560 or Frequency == 603):
        pyautogui.press('right')
    	print("Low D")
    else:
    	print ("Frequency: ",Frequency)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")

frames = []
frequencies = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# Takes data from stream over duration of 1024 frames(Chunk Size)
    data = stream.read(CHUNK)
# Adds Data to frame for save to .wav file
    frames.append(data)
# Adds Data to frame for save to Frequency file
    Frequency=Pitch(data)
    noteFinder(Frequency)
    frequencies.append(Frequency)
print("finished recording")


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()