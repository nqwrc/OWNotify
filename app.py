from tkinter import (BOTH, FLAT, GROOVE, SUNKEN, Button, Frame, Label, Tk, Y,
                     messagebox)

import requests 
from numpy import asarray_chkfinite, sum

from wincap import WindowCapture

url = "INSERT_WEBHOOK_HERE"


data = {
    "username": "Queue Notifier",
    "embeds": [
        {
            "description": "Game found !"
            }
        ],
}

timer = 1000

queue_min, queue_max = 2200, 3110 # windowed : 2645 / borderless : 3092
found_min, found_max = 3380, 4400 # windowed : 3684 / borderless : 4392

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.title("ow-notifier")
        self.resizable(0, 0)
        self.geometry("+%d+%d" % (self.x, self.y + 25))
        self.iconbitmap('ow-notifier.ico')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        menu = Frame(self)
        menu.pack(fill=BOTH, expand=1)

        self.start_btn = Button(menu, text="Start", width=20, height=2,
            relief=GROOVE, cursor='hand2', overrelief=SUNKEN, command=self.start)
        self.start_btn.pack(fill=Y, pady=3)

        # Used to fit queue status (IN QUEUE, MATCH FOUND)
        self.state = Label(menu, width=20, height=1, relief=FLAT)
        self.state.pack(pady=3)

        self.after(timer, self.scanning)

    def scanning(self):
        if self.running:
            self.startDetection()
        self.after(timer, self.scanning)

    def start(self):
        self.win = WindowCapture()
        if self.win.hwnd == 0: return
        self.running = True
        self.start_btn.config(text="Running.. Click to Stop", command=self.stop)

    def stop(self):
        self.running = False
        self.attributes('-topmost', 0)
        self.state.config(text="", bg='#F0F0F0', relief=FLAT)
        self.start_btn.config(text="Start", bg='#F0F0F0', command=self.start)

    def startDetection(self):
        self.attributes('-topmost', 1)

        try:
            self.img = self.win.screenshot()
        except Exception as e:
            messagebox.showerror("Capture error", e)
            self.stop()
            return

        if self.running == 0: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

        else: self.compare()

    def compare(self):
        img = asarray_chkfinite(self.img)
        pixels = sum(img == 255) # white pixels

        print("pixels =", pixels)

        if self.win.state == 2:
            self.stop()
            messagebox.showerror("Error", "\tOverwatch is set to fullscreen.\n\nTo switch between modes, press Shift + Enter")
            return

        elif pixels > queue_min and pixels < queue_max:
            self.state.config(text="Queue detected !", bg='#7CFC00', relief=GROOVE)

        elif pixels > found_min and pixels < found_max:
            self.stop()
            self.state.config(text="Match found !", bg='#B200FF', relief=GROOVE)
            self.sendMessage()

        else: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

    def sendMessage(self):
        result = requests.post(url, json=data)

        if 200 <= result.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
