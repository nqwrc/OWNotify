# OWNotify <img text="Overwatch Icon by Fengquan Li" align="right" src="https://i.postimg.cc/4dGqzJKs/ow.png">

A simple tool for Overwatch that sends you a notification on your phone when you finally get queued into a game. Works with every gamemode, not just competitive.

Download the latest release from <a class="github-button" href="https://github.com/crownium/OWNotify/releases/download/v1.1/OWNotify.zip" data-icon="octicon-download" data-size="large" aria-label="Download crownium/OWNotify on GitHub">GitHub</a> or <a class="github-button" href="https://mega.nz/file/bGw0lZSJ#Jx7zBFljlZ6e5NtL7N0g6CwBhQVqps_mNSB-_HvBQa4" data-icon="octicon-download" data-size="large" aria-label="Download crownium/OWNotify on GitHub">MEGA.NZ</a> .

If you encounter any problems, download the [debug](https://github.com/crownium/OWNotify/releases/download/v1.1/OWNotify-debug.zip) version and contact me if needed.

Supported services :

- Whatsapp
- SMS

## Works with Windowed, Borderless and Fullscreen mode.

---

## REQUIREMENTS

In order to receive the notification, you will need to sign up at [Twilio's website](https://www.twilio.com/try-twilio). After that navigate to the [Twilio console](https://www.twilio.com/console) to request a trial number for receiving SMS.

<!-- <img align="right" src="https://i.postimg.cc/85dpc4rQ/console.png" height=250> -->

If you prefer whatsapp, after signing up follow [this link](https://www.twilio.com/console/sms/whatsapp/learn). A different number will be given to you for receiving WhatsApp messages.

From the twilio console, grab your informations such as your <u>account sid</u>, <u>auth token</u>, <u>phone number</u> and paste them inside the file `config.ini`


```c
// Type phone numbers in this format
from_sms = +12058399217
from_whatsapp = +14155238886
to = YOUR_NUMBER
```

## HOW TO USE

>><img align="right" src="https://i.postimg.cc/g0FrdtxH/demo.png">

1.) Download the latest binary zip from [github](https://github.com/crownium/OWNotify/releases/download/v1.1/OWNotify.zip) or [mega.nz](https://mega.nz/file/bGw0lZSJ#Jx7zBFljlZ6e5NtL7N0g6CwBhQVqps_mNSB-_HvBQa4) and extract it.

3.) Copy your Twilio informations inside the file `config.ini`.

4.) Open `OWNotify.exe` and press "Start".

Now switch over to Overwatch and start your queue !

If the green button __Queue detected__ pops up, then you know everything is working and you can leave your pc and do whatever you prefer while waiting for that long DPS queue.

---

### Note for <ins>_windowed mode_</ins> only

You can keep Overwatch in the background, just make sure that it's not minimized. To avoid that, you can select `Auto restore window when minimized` inside the program's settings.
