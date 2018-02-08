from bots import checkerBot, wolframBot, googleBot
from time import sleep

last_update_id = None


def inlineCommand(updates):
    for update in updates["result"]:
        try:
            if(update["inline_query"]["query"] != None):
                text = update["inline_query"]["query"]
                chat_id = update["inline_query"]["from"]["id"]
                sendMessage("Sry cannot search for: " + text + ". This method isn't working yet. Use /ask instead.", chat_id)
            else:
                text, chat_id = checkerBot.get_last_chat_id_and_text(updates)
                if text.startswith("/start"):
                    sendMessage("Hey " + update["message"]["from"]["first_name"], chat_id)
                elif text.startswith("/ask"):
                    sendMessage(wolframBot.ask(text), chat_id)
                elif text.startswith("/google"):
                    sendMessage(googleBot.googleSearch(text), chat_id)
        except Exception as e:
            print(update)


def sendMessage(text, chat_id):
    checkerBot.send_message(text, chat_id)


def getMessage():
    global last_update_id
    updates = checkerBot.get_updates(last_update_id)
    if len(updates["result"]) > 0:
        last_update_id = checkerBot.get_last_update_id(updates) + 1
        inlineCommand(updates)


def main():
    while True:
        getMessage()
        sleep(0.5)


if __name__ == '__main__':
    main()
