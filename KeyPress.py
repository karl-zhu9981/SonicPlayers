import ctypes

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

''''''
class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))


class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1



def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    raise TypeError('Cannot create INPUT structure!')

XBUTTON1 = 0x0001
XBUTTON2 = 0x0002

VK_CANCEL = 0x03  # Control-break processing
VK_BACK = 0x08  # BACKSPACE key
VK_TAB = 0x09  # TAB key
VK_CLEAR = 0x0C  # CLEAR key
VK_RETURN = 0x0D  # ENTER key
VK_ESCAPE = 0x1B  # ESC key
VK_SPACE = 0x20  # SPACEBAR

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


'''DirectX Key Codes for Letters and Numbers'''
DIK_1 = 0x02
DIK_2 = 0x03
DIK_3 = 0x04
DIK_4 = 0x05
DIK_5 = 0x06
DIK_6 = 0x07
DIK_7 = 0x08
DIK_8 = 0x09
DIK_9 = 0x0A
DIK_0 = 0x0B

DIK_A = 0x1E
DIK_B = 0x30
DIK_C = 0x2E
DIK_D = 0x20
DIK_E = 0x12
DIK_F = 0x21
DIK_G = 0x22
DIK_H = 0x23
DIK_I = 0x17
DIK_J = 0x24
DIK_K = 0x25
DIK_L = 0x26
DIK_M = 0x32
DIK_N = 0x31
DIK_O = 0x18
DIK_P = 0x19
DIK_Q = 0x10
DIK_R = 0x13
DIK_S = 0x1F
DIK_T = 0x14
DIK_U = 0x16
DIK_V = 0x2F
DIK_W = 0x11
DIK_X = 0x2D
DIK_Y = 0x15
DIK_Z = 0x2C

DIK_UP = 0xC8    # UpArrow on arrow keypad */
DIK_PRIOR = 0xC9  # PgUp on arrow keypad */
DIK_LEFT = 0xCB   # LeftArrow on arrow keypad */
DIK_RIGHT = 0xCD  # RightArrow on arrow keypad */
DIK_END = 0xCF    # End on arrow keypad */
DIK_DOWN = 0xD0   # DownArrow on arrow keypad */

'''Not Windows Key Codes'''
VK_ESCAPE = 0x1B  # ESC key
VK_SPACE = 0x20  # SPACEBAR
VK_LEFT = 0xCB  # LEFT ARROW key
VK_UP = 0x26  # UP ARROW key
VK_RIGHT = 0xCD  # RIGHT ARROW key
VK_DOWN = 0x28  # DOWN ARROW key


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
KEY_A = 0x41
KEY_B = 0x42
KEY_C = 0x43
KEY_D = 0x44
KEY_E = 0x45
KEY_F = 0x46
KEY_G = 0x47
KEY_H = 0x48
KEY_I = 0x49
KEY_J = 0x4A
KEY_K = 0x4B
KEY_L = 0x4C
KEY_M = 0x4D
KEY_N = 0x4E
KEY_O = 0x4F
KEY_P = 0x50
KEY_Q = 0x51
KEY_R = 0x52
KEY_S = 0x53
KEY_T = 0x54
KEY_U = 0x55
KEY_V = 0x56
KEY_W = 0x57
KEY_X = 0x58
KEY_Y = 0x59
KEY_Z = 0x5A

'''Functions start here'''
def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)


def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF,
                         parameter & 0xFFFF,
                         parameter >> 16 & 0xFFFF)

def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))


def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))
