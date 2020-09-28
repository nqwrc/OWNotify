from ctypes import (POINTER, Structure, Union, WinDLL, WinError, byref, c_int,
                    c_long, c_uint, c_ulong, c_ulonglong, c_ushort,
                    get_last_error, sizeof)

user32 = WinDLL('user32', use_last_error=True)
VK_MENU               = 0x12
VK_RETURN             = 0x0D
INPUT_KEYBOARD        = 1
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004

WORD      = c_ushort
DWORD     = c_ulong
LONG      = c_long
ULONG_PTR = c_ulonglong # ctypes.u_long
UINT      = c_uint

MAPVK_VK_TO_VSC = 0

class MOUSEINPUT(Structure):
    _fields_ = (("dx", LONG),
                ("dy", LONG),
                ("mouseData", DWORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR))

class KEYBDINPUT(Structure):
    _fields_ = (("wVk", WORD),
                ("wScan", WORD),
                ("dwFlags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(Structure):
    _fields_ = (("uMsg", DWORD),
                ("wParamL", WORD),
                ("wParamH", WORD))

class INPUT(Structure):
    class _INPUT(Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type", DWORD),
                ("_input", _INPUT))

LPINPUT = POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise WinError(get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (UINT, # nInputs
                             LPINPUT,       # pInputs
                             c_int)  # cbSize

# Functions
def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, byref(x), sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, byref(x), sizeof(x))

def FullscreenToWindowed():
    PressKey(VK_MENU)
    PressKey(VK_RETURN)
    ReleaseKey(VK_MENU)
    ReleaseKey(VK_RETURN)
