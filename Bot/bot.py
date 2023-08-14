import logging
import time
import requests
import os
from gpt4all import GPT4All
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')
LLM = os.getenv('LLM')

MODEL = GPT4All(LLM)

# URL für die Telegram Bot API
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

# Funktion zum Senden einer Nachricht
def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, params=params)
    return response.json()

# Funktion zum Verarbeiten der eingehenden Nachrichten
def process_message(message):
    chat_id = message['chat']['id']
    received_text = message['text']
    logger.debug(f"Empfangene Nachricht: {received_text}")
    output = MODEL.generate(received_text, max_tokens=4000, temp=0.2,top_k=40, top_p=0.4, repeat_penalty=1.18)
    logger.debug(f"Antwort: {output}")
    send_message(chat_id, output)

# Funktion zum Abrufen der neuesten Updates
def get_updates(offset=None):
    url = BASE_URL + 'getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

# Hauptfunktion
def main():
    last_update_id = None
    while True:
        try:
            updates = get_updates(offset=last_update_id)
            if updates['ok'] and updates['result']:
                for update in updates['result']:
                    last_update_id = update['update_id'] + 1
                    if 'message' in update:
                        process_message(update['message'])
        except Exception as e:
            print("Error:", str(e))
        
        time.sleep(5)


if __name__ == '__main__':
    main()