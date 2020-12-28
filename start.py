import threading

from saltybot import start_salty_bot, stop_salty_bot, get_bets
from web import start_web_gui
        
        


if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_salty_bot)
    bot_thread.start()
    start_web_gui()
    stop_salty_bot()