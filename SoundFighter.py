import pyaudio
#from KeyPress import *
from matplotlib.mlab import find
import numpy as np
import math
import time
import ctypes



VK_LBUTTON = 0x01               # Left mouse button
VK_RBUTTON = 0x02               # Right mouse button
VK_CANCEL = 0x03                # Control-break processing
VK_MBUTTON = 0x04               # Middle mouse button (three-button mouse)
VK_XBUTTON1 = 0x05              # X1 mouse button
VK_XBUTTON2 = 0x06              # X2 mouse button
VK_BACK = 0x08                  # BACKSPACE key
VK_TAB = 0x09                   # TAB key
VK_CLEAR = 0x0C                 # CLEAR key
VK_RETURN = 0x0D                # ENTER key
VK_SHIFT = 0x10                 # SHIFT key
VK_CONTROL = 0x11               # CTRL key
VK_MENU = 0x12                  # ALT key
VK_PAUSE = 0x13                 # PAUSE key
VK_CAPITAL = 0x14               # CAPS LOCK key
VK_KANA = 0x15                  # IME Kana mode
VK_HANGUL = 0x15                # IME Hangul mode
VK_JUNJA = 0x17                 # IME Junja mode
VK_FINAL = 0x18                 # IME final mode
VK_HANJA = 0x19                 # IME Hanja mode
VK_KANJI = 0x19                 # IME Kanji mode
VK_ESCAPE = 0x1B                # ESC key
VK_CONVERT = 0x1C               # IME convert
VK_NONCONVERT = 0x1D            # IME nonconvert
VK_ACCEPT = 0x1E                # IME accept
VK_MODECHANGE = 0x1F            # IME mode change request
VK_SPACE = 0x20                 # SPACEBAR
VK_PRIOR = 0x21                 # PAGE UP key
VK_NEXT = 0x22                  # PAGE DOWN key
VK_END = 0x23                   # END key
VK_HOME = 0x24                  # HOME key
VK_LEFT = 0xCB                  # LEFT ARROW key
VK_UP = 0xC8                    # UP ARROW key
VK_RIGHT = 0xCD                 # RIGHT ARROW key
VK_DOWN = 0xD0                  # DOWN ARROW key
VK_SELECT = 0x29                # SELECT key
VK_PRINT = 0x2A                 # PRINT key
VK_EXECUTE = 0x2B               # EXECUTE key
VK_SNAPSHOT = 0x2C              # PRINT SCREEN key
VK_INSERT = 0x2D                # INS key
VK_DELETE = 0x2E                # DEL key
VK_HELP = 0x2F                  # HELP key
VK_LWIN = 0x5B                  # Left Windows key (Natural keyboard)
VK_RWIN = 0x5C                  # Right Windows key (Natural keyboard)
VK_APPS = 0x5D                  # Applications key (Natural keyboard)
VK_SLEEP = 0x5F                 # Computer Sleep key
VK_NUMPAD0 = 0x60               # Numeric keypad 0 key
VK_NUMPAD1 = 0x61               # Numeric keypad 1 key
VK_NUMPAD2 = 0x62               # Numeric keypad 2 key
VK_NUMPAD3 = 0x63               # Numeric keypad 3 key
VK_NUMPAD4 = 0x64               # Numeric keypad 4 key
VK_NUMPAD5 = 0x65               # Numeric keypad 5 key
VK_NUMPAD6 = 0x66               # Numeric keypad 6 key
VK_NUMPAD7 = 0x67               # Numeric keypad 7 key
VK_NUMPAD8 = 0x68               # Numeric keypad 8 key
VK_NUMPAD9 = 0x69               # Numeric keypad 9 key
VK_MULTIPLY = 0x6A              # Multiply key
VK_ADD = 0x6B                   # Add key
VK_SEPARATOR = 0x6C             # Separator key
VK_SUBTRACT = 0x6D              # Subtract key
VK_DECIMAL = 0x6E               # Decimal key
VK_DIVIDE = 0x6F                # Divide key
VK_F1 = 0x70                    # F1 key
VK_F2 = 0x71                    # F2 key
VK_F3 = 0x72                    # F3 key
VK_F4 = 0x73                    # F4 key
VK_F5 = 0x74                    # F5 key
VK_F6 = 0x75                    # F6 key
VK_F7 = 0x76                    # F7 key
VK_F8 = 0x77                    # F8 key
VK_F9 = 0x78                    # F9 key
VK_F10 = 0x79                   # F10 key
VK_F11 = 0x7A                   # F11 key
VK_F12 = 0x7B                   # F12 key
VK_F13 = 0x7C                   # F13 key
VK_F14 = 0x7D                   # F14 key
VK_F15 = 0x7E                   # F15 key
VK_F16 = 0x7F                   # F16 key
VK_F17 = 0x80                   # F17 key
VK_F18 = 0x81                   # F18 key
VK_F19 = 0x82                   # F19 key
VK_F20 = 0x83                   # F20 key
VK_F21 = 0x84                   # F21 key
VK_F22 = 0x85                   # F22 key
VK_F23 = 0x86                   # F23 key
VK_F24 = 0x87                   # F24 key
VK_NUMLOCK = 0x90               # NUM LOCK key
VK_SCROLL = 0x91                # SCROLL LOCK key
VK_LSHIFT = 0xA0                # Left SHIFT key
VK_RSHIFT = 0xA1                # Right SHIFT key
VK_LCONTROL = 0xA2              # Left CONTROL key
VK_RCONTROL = 0xA3              # Right CONTROL key
VK_LMENU = 0xA4                 # Left MENU key
VK_RMENU = 0xA5                 # Right MENU key
VK_BROWSER_BACK = 0xA6          # Browser Back key
VK_BROWSER_FORWARD = 0xA7       # Browser Forward key
VK_BROWSER_REFRESH = 0xA8       # Browser Refresh key
VK_BROWSER_STOP = 0xA9          # Browser Stop key
VK_BROWSER_SEARCH = 0xAA        # Browser Search key
VK_BROWSER_FAVORITES = 0xAB     # Browser Favorites key
VK_BROWSER_HOME = 0xAC          # Browser Start and Home key
VK_VOLUME_MUTE = 0xAD           # Volume Mute key
VK_VOLUME_DOWN = 0xAE           # Volume Down key
VK_VOLUME_UP = 0xAF             # Volume Up key
VK_MEDIA_NEXT_TRACK = 0xB0      # Next Track key
VK_MEDIA_PREV_TRACK = 0xB1      # Previous Track key
VK_MEDIA_STOP = 0xB2            # Stop Media key
VK_MEDIA_PLAY_PAUSE = 0xB3      # Play/Pause Media key
VK_LAUNCH_MAIL = 0xB4           # Start Mail key
VK_LAUNCH_MEDIA_SELECT = 0xB5   # Select Media key
VK_LAUNCH_APP1 = 0xB6           # Start Application 1 key
VK_LAUNCH_APP2 = 0xB7           # Start Application 2 key
VK_OEM_1 = 0xBA                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the ';:' key
VK_OEM_PLUS = 0xBB              # For any country/region, the '+' key
VK_OEM_COMMA = 0xBC             # For any country/region, the ',' key
VK_OEM_MINUS = 0xBD             # For any country/region, the '-' key
VK_OEM_PERIOD = 0xBE            # For any country/region, the '.' key
VK_OEM_2 = 0xBF                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the '/?' key
VK_OEM_3 = 0xC0                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the '`~' key
VK_OEM_4 = 0xDB                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the '[{' key
VK_OEM_5 = 0xDC                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the '\|' key
VK_OEM_6 = 0xDD                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the ']}' key
VK_OEM_7 = 0xDE                 # Used for miscellaneous characters; it can vary by keyboard.
                                # For the US standard keyboard, the 'single-quote/double-quote' key
VK_OEM_8 = 0xDF                 # Used for miscellaneous characters; it can vary by keyboard.
VK_OEM_102 = 0xE2               # Either the angle bracket key or the backslash key on the RT 102-key keyboard
VK_PROCESSKEY = 0xE5            # IME PROCESS key
VK_PACKET = 0xE7                # Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KEYUP
VK_ATTN = 0xF6                  # Attn key
VK_CRSEL = 0xF7                 # CrSel key
VK_EXSEL = 0xF8                 # ExSel key
VK_EREOF = 0xF9                 # Erase EOF key
VK_PLAY = 0xFA                  # Play key
VK_ZOOM = 0xFB                  # Zoom key
VK_PA1 = 0xFD                   # PA1 key
VK_OEM_CLEAR = 0xFE             # Clear key

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

KEY_0 = 0x30
KEY_1 = 0x31
KEY_2 = 0x32
KEY_3 = 0x33
KEY_4 = 0x34
KEY_5 = 0x35
KEY_6 = 0x36
KEY_7 = 0x37
KEY_8 = 0x38
KEY_9 = 0x39
KEY_A = 0x1E
KEY_B = 0x42
KEY_C = 0x43
KEY_D = 0x20
KEY_E = 0x12
KEY_F = 0x46
KEY_G = 0x47
KEY_H = 0x48
KEY_I = 0x17
KEY_J = 0x24
KEY_K = 0x25
KEY_L = 0x26
KEY_M = 0x4D
KEY_N = 0x4E
KEY_O = 0x4F
KEY_P = 0x50
KEY_Q = 0x10
KEY_R = 0x52
KEY_S = 0x1F
KEY_T = 0x54
KEY_U = 0x55
KEY_V = 0x56
KEY_W = 0x11
KEY_X = 0x2D
KEY_Y = 0x59
KEY_Z = 0x2C



LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

''''''
# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
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
	if ((freq > 946  and freq < 992) or (freq > 482 and freq < 506)):
#	print("b")
		return "b"
	elif ((freq > 860 and freq < 884) or (freq > 429 and freq < 453)):
#	print("a")
		return "a"
	elif ((freq > 774 and freq < 798 )or (freq > 387 and freq < 405)  or (freq > 1570 and freq < 1595)  ):
#	print("g")
		return "g"
	elif ((freq > 731 and freq < 755) or (freq > 355 and freq < 379)  or (freq > 1460 and freq < 1510) ):
#	print("f#")
		return "f#"
	elif ((freq > 645 and freq < 690)or (freq > 319 and freq < 339)or (freq > 1300 and freq < 1339)):
#	print("e")
		return "e"
	elif ((freq > 555 and freq <604)or (freq > 280 and freq < 304)):
#	print ("Low D")
		return "d"

	elif ((freq > 1141 and freq < 1185) or (freq > 1740 and freq < 1790) ):
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
				elif (note == "d"):
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
				elif (note == "d"):
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