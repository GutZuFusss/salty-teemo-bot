import sys
import irc.bot
import requests
import time

BET_BOT_NAME = 'xxsaltbotxx'
BET_MSG_TRIGGER = 'Bet complete'
PRE_BET_AMOUNT = ', '
POST_BET_AMOUNT = '. Your'

class SaltyBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel, web_app):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        self.web_app = web_app

        self.last_bet = time.time() - 9999999; # xd clean
        self.shrooms_red = 0
        self.shrooms_blue = 0

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

        self.start()


    def handle_bet(self, s):
        if time.time() - self.last_bet > 300:
            self.shrooms_red = 0
            self.shrooms_blue = 0
            self.web_app.reset_bets()


        self.last_bet = time.time();

        amount = int(s[s.find(PRE_BET_AMOUNT)+len(PRE_BET_AMOUNT):s.rfind(POST_BET_AMOUNT)])
        if 'RED' in s:
            self.shrooms_red += amount
        if 'BLUE' in s:
            self.shrooms_blue += amount

        print('#####################################')
        print('RED:  ' + str(self.shrooms_red))
        print('BLUE: ' + str(self.shrooms_blue))
        print('#####################################')

        self.web_app.update_bets(self.get_bets())


    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.join(self.channel)


    def on_pubmsg(self, c, e):
        msg =  e.arguments[0]
        nick = e.source.nick
        print('[recv] "' + nick + '": ' + e.arguments[0])

        if nick == BET_BOT_NAME and BET_MSG_TRIGGER in msg:
            self.handle_bet(msg)

    def get_bets(self):
        return [self.shrooms_red, self.shrooms_blue] # TODO: ret this as a map
