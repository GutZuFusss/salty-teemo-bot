import sys
import irc.bot
import requests
import time
import json

from web import update_bets, reset_bets


class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

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


    def handle_bet(self, s):
        if time.time() - self.last_bet > 300:
            self.shrooms_red = 0
            self.shrooms_blue = 0
            reset_bets()


        self.last_bet = time.time();

        amount = int(s[s.find(", ")+len(", "):s.rfind(". Your")])
        if "RED" in s:
            self.shrooms_red += amount
        if "BLUE" in s:
            self.shrooms_blue += amount

        print('#####################################')
        print('RED:  ' + str(self.shrooms_red))
        print('BLUE: ' + str(self.shrooms_blue))
        print('#####################################')

        update_bets([self.shrooms_red, self.shrooms_blue])


    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.join(self.channel)


    def on_pubmsg(self, c, e):
        msg =  e.arguments[0]
        nick = e.source.nick
        print('[recv] "' + nick + '": ' + e.arguments[0])

        if nick == "xxsaltbotxx" and "Bet complete" in msg:
            self.handle_bet(msg)


with open('config.json', 'r') as f: # TODO: this should def not be done here xd
    config = json.load(f)
username  = config['username']
client_id = config['client_id']
token     = config['token']
channel   = 'saltyteemo'
bot = TwitchBot(username, client_id, token, channel)

def start_salty_bot():
    bot.start()

def stop_salty_bot():
    bot.die()

def get_bets():
    return [bot.shrooms_red, bot.shrooms_blue]