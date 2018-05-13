import json
import requests
import time
import urllib
import re
import wolframalpha

WOLFRAM_TOKEN = "9HL4GP-LLTREW7G52"
TOKEN = "397055226:AAEqsVgAmc3URoobKaIceVyIGicp38zuutc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset = None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            #TODO: Fixa så att det bara går att starta en gång, genom att ex. skaffa en databas där alla registrerade användare finns.
            if text.startswith("/start"):
                send_message("Hey " + update["message"]["from"]["first_name"], chat)
                break
            elif text.startswith("/ask"):
                text = re.sub("/ask ", "", text, count=1)
                send_message("Loading result for: " + text, chat)
                text = wolfram_checker(text)
            response = bot.get_response(text)
            print(response)
            send_message(text, chat)
        except Exception as e:
            print(e)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def wolfram_checker(text):
    client = wolframalpha.Client(WOLFRAM_TOKEN)
    res = client.query(text)
    answer = ""
    for pod in res.pods:
        answer += str(pod.text) + "\n"
    return answer

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates)+1
            echo_all(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
