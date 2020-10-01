# OWNotify - Now working in FULLSCREEN !

A simple tool for Overwatch that sends you a notification on your phone when you finally get queued into a game. Works with every gamemode, not just competitive.

Download the latest release from <a class="github-button" href="https://github.com/crownium/OWNotify/releases/download/v1.1/OWNotify.zip" data-icon="octicon-download" data-size="large" aria-label="Download crownium/OWNotify on GitHub">GitHub</a> or <a class="github-button" href="https://mega.nz/file/bGw0lZSJ#Jx7zBFljlZ6e5NtL7N0g6CwBhQVqps_mNSB-_HvBQa4" data-icon="octicon-download" data-size="large" aria-label="Download crownium/OWNotify on GitHub">MEGA.NZ</a> .

If you encounter any problems, download the [debug](https://mega.nz/file/zXx0hbJS#MNwpw4SgcneNJZhdwbrg2YuDlaFwRJAtg3ZaY5ki_ms) version and contact me if needed.

Supported services :

- Whatsapp
- SMS

**(NOTE - Works with Windowed, Borderless and Fullscreen !!! )**

---

## REQUIREMENTS

In order to receive the notification, you will need to sign up at [Twilio's website](https://www.twilio.com/try-twilio). After that navigate to the [Twilio console](https://www.twilio.com/console) to request a trial number for receiving SMS.

<!-- <img align="right" src="https://i.postimg.cc/85dpc4rQ/console.png" height=250> -->

If you prefer whatsapp, after signing up follow [this](https://www.twilio.com/console/sms/whatsapp/learn) link. A different number will be given to you for receiving WhatsApp messages.

Grab your informations such as your <u>account sid</u> , <u>auth token</u> and <u>phone number</u>, you will need to paste them inside the file `config.ini`


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

Now switch over to Overwatch and start your queue!

If the green button "Queue detected" pops up, then you know everything's working and you can start being productive while waiting for that long DPS queue!

---

### Note ( for windowed mode only )

You don't need to keep Overwatch as your top window, just make sure that it's not minimized. To avoid that, you can select `Auto restore window when minimized` inside the program's settings.
