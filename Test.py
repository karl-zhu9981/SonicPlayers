
import pyaudio
import wave
import KeyPress
from matplotlib.mlab import find
import numpy as np
import math

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()


#Turns raw audio input into frequency data
def Pitch(signal):
    signal = np.fromstring(signal, 'Int16')
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing))
    f0=round (len(index) *RATE / (2*np.prod( len(signal))))
    return f0

def noteFinder(freq):
    if (freq > 2900 and freq < 3000):
        print("b")
    elif (freq == 2627 or freq == 2606 or freq == 2649 or freq == 2584):
        print("a")
#        SendInput(Keyboard(VK_RIGHT))
    elif (freq == 2326 or freq == 2304 or freq == 2347 or freq == 2369):
        print("g")
 #       SendInput(Keyboard(VK_LEFT, KEYEVENTF_KEYUP))
    elif (freq == 2218 or freq == 2196 or freq == 2261):
        print("f#")
    elif (freq == 646 or freq == 668 or freq == 689):
        print("e")
    elif (freq == 581 or freq == 560 or freq == 603):
        print("Low D")
    else:
        print("Frequency: ", freq)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print("recording...")

frames = []
frequencies = []
counter ={}
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
# Takes data from stream over duration of 1024 frames(Chunk Size)
    data = stream.read(CHUNK)
# Adds Data to frame for save to .wav file
    frames.append(data)
# Adds Data to frame for save to Frequency file
    freq=Pitch(data)
    noteFinder(freq)
    frequencies.append(freq)
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