from tkinter import messagebox

from numpy import ascontiguousarray, fromstring
from pythonwin.win32ui import CreateBitmap, CreateDCFromHandle
from win32.win32gui import (DeleteObject, FindWindow, GetWindowDC,
                            GetWindowPlacement, GetWindowRect, ReleaseDC,
                            ShowWindow)

from keypress import FullscreenToWindowed

SW_MAXIMIZE = 3
SRCCOPY = 13369376

class WindowCapture:
    def __init__(self, window_name="Overwatch"):
        self.hwnd = FindWindow(None, window_name)
        if not self.hwnd:
            messagebox.showerror("404", "{} window not found".format(window_name))
            return
        ShowWindow(self.hwnd, SW_MAXIMIZE)

    def computeBox(self):
        window_rect = GetWindowRect(self.hwnd)

        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]
        self.w = self.width - 16
        self.h = self.height - 38

        if self.width == 1920 and self.height == 1080:
            self.isFullscreen = True
            adjust = (0,)*4
        else:
            self.isFullscreen = False
            adjust = (-2, 2, 0, 27)

        self.box_w = round(self.w // 6.3) + adjust[0]
        self.box_h = round(self.h // 11.8) + adjust[1]
        self.box_x = round(self.w // 2.352) + adjust[2]
        self.box_y = round(self.h // 23.5) + adjust[3]
        # print(self.w, self.h)
        # print("w :", self.box_w, "h :", self.box_h)
        # print("x :", self.box_x, "y :", self.box_y)

    def exitFullscreen(self):
        FullscreenToWindowed()
        ShowWindow(self.hwnd, SW_MAXIMIZE)

    def toggleMax(self, var=0):
        if var == 1:
            flags, state, ptMin, ptMax, rect = GetWindowPlacement(self.hwnd)
            if state == 2: ShowWindow(self.hwnd, SW_MAXIMIZE)
            # if rect[0] >= 1 and rect[1] >= 1:
            #     ShowWindow(self.hwnd, SW_MAXIMIZE)

    def screenshot(self):
        self.computeBox()

        wDC = GetWindowDC(self.hwnd)
        dcObj = CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = CreateBitmap()

        try: dataBitMap.CreateCompatibleBitmap(dcObj, self.box_w, self.box_h)
        except Exception as e:
            messagebox.showerror(e)
            return

        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.box_w, self.box_h), dcObj, (self.box_x, self.box_y), SRCCOPY)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.box_h, self.box_w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        ReleaseDC(self.hwnd, wDC)
        DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]
        img = ascontiguousarray(img)

        return img

    # def boxMinMatch(self):
    #     percent = [60, 70, 77, 85, 120]
    #     min_match = [5, 7, 14, 30, 40]

    #     for item in percent:
    #         w_percent = self.width*100/1920
    #         h_percent = self.height*100/1080
    #         if w_percent <= item or h_percent <= item:
    #             # print("W :", format(w_percent, '.2f')+"%", "H :", format(h_percent, '.2f')+"%")
    #             # print("% arr :", item, "%")
    #             print(min_match[percent.index(item)])
    #             return min_match[percent.index(item)]

