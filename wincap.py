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

p1080 = (('fullscreen', (1920, 1080)), ('windowed', ((1936, 1056))))
c_w, c_h, c_x, c_y = 6.3, 11.8, 2.352, 23.5
border, titlebar = 16, 38

class WindowCapture:

    def __init__(self, window_name="Overwatch"):
        self.hwnd = FindWindow(None, window_name)
        threadid, self.pid  = GetWindowThreadProcessId(self.hwnd)

        if not self.hwnd:
            messagebox.showerror("404", "Run {} before pressing Start !".format(window_name))
            return
        ShowWindow(self.hwnd, SW_MAXIMIZE)

    def calcBox(self, w, h):
        if ((w, h) == (p1080[0][1])): adj = (0,)*4
        else : adj = (-2, 2, 0, 27)

        w, h = w - border, h - titlebar
        w, h, x, y = round(w // c_w), round(h // c_h), round(w // c_x), round(h // c_y)

        return w + adj[0], h + adj[1], x + adj[2], y + adj[3]

    def computeBox(self):
        left, top, right, bottom = GetWindowRect(self.hwnd)
        flags, self.state, ptMin, ptMax, rect = GetWindowPlacement(self.hwnd)
        self.w, self.h = right - left, bottom - top
        # print(self.w, self.h)
        # print(left, top, right, bottom, rect)
        # print(flags, self.state, ptMin, ptMax, rect)

        # print(self.fullscreen)
        return self.calcBox(self.w, self.h)

    def screenshot(self, var=0):
        w, h, x, y = self.computeBox()

        wDC = GetWindowDC(self.hwnd)        
        dcObj = CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = CreateBitmap()

        try: dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        except Exception as e:
            messagebox.showerror(e)
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
