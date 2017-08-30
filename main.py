import checkerBot, wolframBot, googleBot
from time import sleep

def inlineCommand(updates):
    for update in updates["result"]:
        try:
            text, chat_id = checkerBot.get_last_chat_id_and_text(updates)
            if text.startswith("/start"):
                text = "Hey " + update["message"]["from"]["first_name"]
            elif text.startswith("/ask"):
                text = wolframBot.ask(text)
            elif text.startswith("/google"):
                text = googleBot.googleSearch(text)
            checkerBot.send_message(text, chat_id)
        except Exception as e:
            print(e)

def main():
    last_update_id = None
    while True:
        updates = checkerBot.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = checkerBot.get_last_update_id(updates)+1
            inlineCommand(updates)
        sleep(0.5)

if __name__ == '__main__':
    main()
