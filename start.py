import threading
import json

from saltybot import SaltyBot
from web import WebApp

with open('config.json', 'r') as f:
    config = json.load(f)

def init_salty_bot(web):
    username  = config['username']
    client_id = config['client_id']
    token     = config['token']
    channel   = 'saltyteemo'
    return SaltyBot(username, client_id, token, channel, web)

if __name__ == "__main__":
    web_gui = WebApp()
    bot_thread = threading.Thread(target=init_salty_bot, args=(web_gui,))
    bot_thread.start()
    web_gui.start()
    salty_bot.die()
