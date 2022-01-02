from tkinter import messagebox

from numpy import ascontiguousarray, fromstring
from PIL import Image
from pythonwin.win32ui import CreateBitmap, CreateDCFromHandle
from win32.win32gui import (DeleteObject, FindWindow, GetWindowDC,
                            GetWindowPlacement, GetWindowRect, ReleaseDC,
                            ShowWindow)
from win32.win32process import GetWindowThreadProcessId
import win32gui

SW_MAXIMIZE = 3
SRCCOPY = 13369376

borderless_mode = (1920, 1080)
windowed_mode = (1936, 1056)

width_threshold = 1900

point__w, point__h, point__x, point__y = 6.3, 11.8, 2.352, 23.5
border, titlebar = 16, 38

class WindowCapture:

    def __init__(self, window_name="Overwatch"):
        self.hwnd = FindWindow(None, window_name)
        threadid, self.pid  = GetWindowThreadProcessId(self.hwnd)

        if not self.hwnd:
            messagebox.showerror("Error", "Run {} first !".format(window_name))
            return

    def calcBox(self, w, h):
        pad__w, pad__h, pad__x, pad__y = (0,)*4

        if (w, h) == windowed_mode: pad__w, pad__h, pad__x, pad__y = -2, 2, 0, 27

        w, h = w - border, h - titlebar
        w, h, x, y = round(w // point__w), round(h // point__h), round(w // point__x), round(h // point__y)

        return w + pad__w, h + pad__h, x + pad__x, y + pad__y

    def computeBox(self):
        left, top, right, bottom = GetWindowRect(self.hwnd)
        flags, self.state, ptMin, ptMax, rect = GetWindowPlacement(self.hwnd)

        self.w, self.h = right - left, bottom - top
        # print(self.w)

        # Maximize window if smaller than threshold
        if self.w < width_threshold:
            ShowWindow(self.hwnd, 3)

        return self.calcBox(self.w, self.h)

    def screenshot(self):
        w, h, x, y = self.computeBox()

        wDC = GetWindowDC(self.hwnd)        
        dcObj = CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = CreateBitmap()

        try: dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        except Exception as e:
            return

        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (x, y), SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = fromstring(signedIntsArray, dtype='uint8')
        img.shape = (h, w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        ReleaseDC(self.hwnd, wDC)
        DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = ascontiguousarray(img)

        return Image.fromarray(img)
