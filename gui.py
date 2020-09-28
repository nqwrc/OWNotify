from tkinter import (BOTH, DISABLED, END, FLAT, GROOVE, SUNKEN, Button,
                     Checkbutton, Frame, IntVar, Label, Radiobutton, StringVar,
                     Tk, Toplevel, W, Y, messagebox)

from numpy import asarray_chkfinite, sum
from PIL import Image

from conf_parser import Parser
from keypress import FullscreenToWindowed
from wincap import WindowCapture

configs = 'config.ini'
time = 1000

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.running = False
        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.title("QP")
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

        self.after(time, self.scanning)


    def scanning(self):
        if self.running: self.startDetection()
        self.after(time, self.scanning)

    def start(self):
        self.win = WindowCapture()
        if self.win.hwnd == 0: return

        self.running = True
        self.start_btn.config(text="Running.. Click to Stop", bg='#7CFC00', command=self.stop)

    def stop(self):
        self.running = False
        self.attributes('-topmost', 0)
        self.state.config(text="", bg='#F0F0F0', relief=FLAT)
        self.start_btn.config(text="Start", bg='#F0F0F0', command=self.start)

    def startDetection(self):
        self.win.toggleMax(self.tggl_max.get())
        self.attributes('-topmost', self.tggl_top.get())

        try:
            self.img = Image.fromarray(self.win.screenshot())

            if self.img.size[0] == 30 and self.img.size[1] == 3:
                raise Exception("Window has been minimized, stopping..")
        except Exception as e:
            messagebox.showerror("Error", e)
            self.stop()
            return

        if self.running == 0: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

        else: self.compare()

    def compare(self):
        if self.win.isFullscreen:
            th = (1750, 2800, 4400, 4500)
        else:
            th = (1400, 2250, 3500, 3800)

        img = asarray_chkfinite(self.img)
        white = sum(img == 255)
        # print(white)

        if white > th[0] and white < th[1]:
            self.state.config(text="Queue detected !", bg='#7CFC00', relief=GROOVE)

        elif white > th[2] and white < th[3]:
            self.stop()
            self.state.config(text="Match found !", bg='#B200FF', relief=GROOVE)
            self.sendMessage()

        else: self.state.config(text="", bg='#F0F0F0', relief=FLAT)

    def sendMessage(self):
        choice = self.msg_var.get()
        if choice == 'Whatsapp':
            self.conf.twilioMsg('whatsapp')
        elif choice == 'SMS':
            self.conf.twilioMsg()
        elif choice == 'Discord':
            self.conf.discordMsg()
        elif choice == 'Telegram':
            self.conf.telegramMsg()

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

    def openSettings(self):
        self.settings = Toplevel()
        self.settings.resizable(0, 0)
        self.settings.title("Settings")
        self.settings.iconbitmap('icons/own.ico')
        self.settings.protocol("WM_DELETE_WINDOW", self.closeSettings)
        self.settings.geometry("+%d+%d" % (self.x, self.y + 165))

        menu = Frame(self.settings)
        menu.grid()

        Checkbutton(menu, text="Auto restore window when minimized",
            variable=self.tggl_max, command=self.tgglGame).grid()

        Checkbutton(menu, text="Stay on top  (only after pressing Start)",
            variable=self.tggl_top, command=self.tgglApp).grid()

        Label(menu, text="Choose your preference :").grid(sticky=W)

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
