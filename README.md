# OWNotify

A simple tool for Overwatch that sends you a notification on your phone when you finally get queued into a game. Works with every gamemode not just competitive.

Supported services :

- Whatsapp
- SMS

**(NOTE - As of now this program only works with Overwatch in Windowed or Borderless Windowed mode)**

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

>><img align="right" padding-inline=25% src="https://i.postimg.cc/g0FrdtxH/demo.png">

1.) Download the binary zip from [github](https://github.com/crownium/OWNotify/releases/download/v0.3/OWNotify.zip) or [mega.nz](https://mega.nz/file/bOom1BaT#EXGxjJz1EhmzqvMjRdNaSHPepuh88HkQi__5IMGXUNk) and extract it.

3.) Copy your Twilio informations inside the file `config.ini`.

4.) Open `OWNotify.exe` and press "Start".

Now switch over to Overwatch and start your queue!

If the green button "Queue detected" pops up, then you know everything's working and you can start being productive while waiting for that long DPS queue!

---

## Note

You don't need to keep Overwatch as your top window, just make sure that it's not minimized. To avoid that, you can select the setting `Auto restore window when minimized` inside the program.
