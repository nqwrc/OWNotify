from configparser import ConfigParser
from os import path

from twilio.rest import Client

configs = 'config.ini'

class Parser(ConfigParser):
    def __init__(self):
        super().__init__()

        if path.isfile(configs): return

        self.read(configs)
        self.add_section('Settings')
        self.set('Settings', 'togglemax', '0')
        self.set('Settings', 'stayontop', '0')
        self.set('Settings', 'message', 'comm_service')

        self.add_section('Discord')
        self.set('Discord', 'token', 'bot_secret_token')
        self.set('Discord', 'userid', 'user_id')

        self.add_section('Twilio')
        self.set('Twilio', 'sid', 'sid_number')
        self.set('Twilio', 'token', 'auth_token')
        self.set('Twilio', 'message', 'game found !')
        self.set('Twilio', 'to', 'your_number')
        self.set('Twilio', 'from_sms', 'sms_number')
        self.set('Twilio', 'from_whatsapp', 'whatsapp_number')

        with open(configs, 'w') as f:
            self.write(f)

    def discordMsg(self):
        # TODO
        print("Send discord message.")
        # Popen(["notify.exe", "{0}".format(self.get('Discord', 'userid'))],
        #         stdin=None, stdout=None, stderr=None, close_fds=True)

    def twilioMsg(self, mode=''):
        self.read(configs)

        sid = self.get('Twilio', 'sid')
        token = self.get('Twilio', 'token')
        message = self.get('Twilio', 'message')
        to_num = self.get('Twilio', 'to')
        from_num = self.get('Twilio', 'from_sms')

        client = Client(sid, token)

        if mode != '':
            mode = 'whatsapp:'
            from_num = self.get('Twilio', 'from_whatsapp')

        message = client.messages.create(body=message,
                    from_=mode+from_num, to=mode+to_num)

        print(message)

    def telegramMsg(self):
        # TODO
        print("Send telegram message.")
