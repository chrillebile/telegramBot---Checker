from bots import checkerBot, wolframBot, googleBot, aiBot
from time import sleep

last_update_id = None


def inlineCommand(updates):
    for update in updates["result"]:
        try:
            text, chat_id = checkerBot.get_last_chat_id_and_text(updates)
            if text.startswith("/start"):
                sendMessage("Hey " + update["message"]["from"]["first_name"], chat_id)
            elif text.startswith("/ask"):
                sendMessage(wolframBot.ask(text), chat_id)
            elif text.startswith("/google"):
                sendMessage(googleBot.googleSearch(text), chat_id)
            else:
                sendMessage(aiBot.getResponse(text, chat_id), chat_id)
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
    print("Starting ai bot training...\n")
    print(aiBot.trainBot())
    print("Now running bot...\n")
    while True:
        try:
            getMessage()
            sleep(0.5)
        except (KeyboardInterrupt, EOFError, SystemExit):
            print("------------------------System failed------------------------")
            break

if __name__ == '__main__':
    main()
