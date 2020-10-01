from tkinter import (BOTH, DISABLED, END, FLAT, GROOVE, SUNKEN, Button,
                     Checkbutton, Frame, IntVar, Label, Radiobutton, StringVar,
                     Tk, Toplevel, W, Y, messagebox)

from numpy import asarray_chkfinite, sum
from PIL import Image
from screen_recorder_sdk import screen_recorder as rec

from conf_parser import Parser
from keypress import FullscreenToWindowed
from wincap import WindowCapture

configs = 'config.ini'
timer = 1000

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.title("OWN")
        self.resizable(0, 0)
        self.geometry("+%d+%d" % (self.x, self.y + 25))
        self.iconbitmap('icons/own.ico')
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        menu = Frame(self)
        menu.pack(fill=BOTH, expand=1)

        self.start_btn = Button(menu, text="Start", width=20, height=2,
            relief=GROOVE, cursor='hand2', overrelief=SUNKEN, command=self.start)
        self.start_btn.pack(fill=Y, pady=3)

        self.config_btn = Button(menu, text="Settings", width=10, height=1,
            relief=GROOVE, cursor='hand2', overrelief=SUNKEN, command=self.openSettings)
        self.config_btn.pack(fill=Y, pady=3)

        self.state = Label(menu, width=20, height=1, relief=FLAT)
        self.state.pack(pady=3)

        # initialize configparser class
        self.conf = Parser()
        self.conf.read(configs)

        # read settings from config file
        self.tggl_max = IntVar()
        self.tggl_max.set(self.conf.get('Settings', 'togglemax'))
        self.tggl_top = IntVar()
        self.tggl_top.set(self.conf.get('Settings', 'stayontop'))
        self.msg_var = StringVar()
        self.msg_var.set(self.conf.get('Settings', 'message'))
        self.set_mode = IntVar()
        self.set_mode.set(self.conf.get('Settings', 'mode'))

        self.after(timer, self.scanning)

    def scanning(self):
        if self.running:
            if self.set_mode.get() == 0:   self.startDetection()
            elif self.set_mode.get() == 1: self.startFullscreen()
        self.after(timer, self.scanning)

    def start(self):
        self.win = WindowCapture()
        if self.win.hwnd == 0: return
        self.initObj()
        self.running = True
        self.start_btn.config(text="Running.. Click to Stop", bg='#7CFC00', command=self.stop)

    def stop(self):
        self.running = False
        self.attributes('-topmost', 0)
        self.state.config(text="", bg='#F0F0F0', relief=FLAT)
        self.start_btn.config(text="Start", bg='#F0F0F0', command=self.start)

    def startDetection(self):
        self.attributes('-topmost', self.tggl_top.get())

        try:
            self.img = self.win.screenshot(self.tggl_max.get())
        except Exception as e:
            messagebox.showerror("Capture error", e)
            self.stop()
            return

        if self.running == 0: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

        else: self.compare()

    def initObj(self):
        if self.set_mode.get() == 1:
            params = rec.RecorderParams()
            params.pid, params.desktop_num = self.win.pid, 0
            rec.init_resources(params)
            self.startFullscreen()

    def startFullscreen(self):
        w, h, x, y = self.win.computeBox()
        try:
            img = rec.get_screenshot(1)
            self.img = img.crop((x, y, w+x, h+y))
            self.compare()
        except Exception as e:
            rec.free_resources()
            self.stop()
            return

    def compare(self):
        if self.win.w == 1920 and self.win.h == 1080:
            thresh = (1750, 2800, 4400, 4500)
        elif (self.win.w, self.win.h) == (1936, 1056):
            thresh = (1400, 2250, 3500, 3800)
        else: thresh = self.win.boxMinMatch()

        img = asarray_chkfinite(self.img)
        white = sum(img == 255)
        # print("white pixels =", white)
        # print("thresh[0]", thresh[0], "thresh[1]", thresh[1], "thresh[2]", thresh[2], "thresh[3]", thresh[3])

        if self.win.state == 2 :
            self.state.config(text="Unable to capture", bg='#FF0000', relief=FLAT)

        elif white > thresh[0] and white < thresh[1]:
            self.state.config(text="Queue detected !", bg='#7CFC00', relief=GROOVE)

        elif white > thresh[2] and white < thresh[3]:
            self.stop()
            self.state.config(text="Match found !", bg='#B200FF', relief=GROOVE)
            self.sendMessage()

        else: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

    def sendMessage(self):
        choice = self.msg_var.get()
        if choice == 'Whatsapp':
            self.conf.twilioMsg('wh')
        elif choice == 'SMS':
            self.conf.twilioMsg()
        # elif choice == 'Discord': self.conf.discordMsg()

    def tgglApp(self):
        self.conf.read(configs)
        self.conf.set('Settings', 'stayontop', str(self.tggl_top.get()))
        with open(configs, 'w') as f: self.conf.write(f)

    def tgglGame(self):
        self.conf.read(configs)
        self.conf.set('Settings', 'togglemax', str(self.tggl_max.get()))
        with open(configs, 'w') as f: self.conf.write(f)

    def msgChoice(self):
        self.conf.read(configs)
        self.conf.set('Settings', 'message', self.msg_var.get())
        with open(configs, 'w') as f: self.conf.write(f)

    def setMode(self):
        self.conf.read(configs)
        self.conf.set('Settings', 'mode', str(self.set_mode.get()))
        with open(configs, 'w') as f: self.conf.write(f)

    def openSettings(self):
        self.settings = Toplevel()
        self.settings.resizable(0, 0)
        self.settings.title("Settings - OWN")
        self.settings.iconbitmap('icons/own.ico')
        self.settings.protocol("WM_DELETE_WINDOW", self.closeSettings)
        self.settings.geometry("+%d+%d" % (self.x, self.y + 165))

        menu = Frame(self.settings)
        menu.grid()

        Checkbutton(menu, text="Auto restore window when minimized",
            variable=self.tggl_max, command=self.tgglGame).grid()

        Checkbutton(menu, text="Keep OWN on top after pressing Start",
            variable=self.tggl_top, command=self.tgglApp).grid()

        Label(menu, text="Choose mode :").grid(sticky=W)

        MODE = [("Windowed/Borderless", 0), ("Fullscreen", 1)]
        for text in MODE:
            Radiobutton(menu, text=text[0], variable=self.set_mode,
                value=text[1], command=self.setMode).grid(sticky=W)

        Label(menu, text="Choose push notification :").grid(sticky=W)

        MODES = ["Whatsapp", "SMS"]
        for text in MODES:
            Radiobutton(menu, text=text, variable=self.msg_var,
                value=text, command=self.msgChoice).grid(sticky=W)

        MODES = ["Discord", "Telegram"]
        for text in MODES:
            Radiobutton(menu, text=text, variable=self.msg_var,
                value=text, state=DISABLED, command=self.msgChoice).grid(sticky=W)

        Button(menu, text="Click to test message", relief=GROOVE,
            cursor='hand2', overrelief=SUNKEN, command=self.sendMessage).grid(pady=3)

        self.conf.set('Settings', 'togglemax', str(self.tggl_max.get()))
        self.conf.set('Settings', 'stayontop', str(self.tggl_top.get()))
        self.conf.set('Settings', 'message', self.msg_var.get())
        self.conf.set('Settings', 'mode', str(self.set_mode.get()))

        self.config_btn.config(command=self.closeSettings)

        self.settings.transient(self)
        self.wait_window(self.settings)

    def closeSettings(self):
        if not self.settings.winfo_exists(): self.openSettings()
        else: self.settings.destroy()

        self.config_btn.config(command=self.openSettings)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
