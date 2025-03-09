print("Загрузка модуля telegram_utils")
from httpx import post
from dotenv import load_dotenv
from pathlib import Path
import os
import paths
os.chdir(paths.project_dir)
load_dotenv("gitignore/.env")

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")


def send_message(text: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = post(url, params=params)
    response_data: dict = response.json()
    message_id = response_data.get('result', {}).get('message_id')
    return message_id

def send_image(image_path: Path, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {"photo": open(image_path, "rb")}
    params = {"chat_id": chat_id, "caption": caption}
    response = post(url, files=files, params=params)
    response_data: dict = response.json()
    message_id = response_data.get('result', {}).get('message_id')
    return message_id

# pinned info message id = 696
def edit_message(new_text, message_id=696):
    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text,
    }
    response = post(url, params=params)
    return response.json()

def edit_caption(new_caption, message_id):
    url = f"https://api.telegram.org/bot{bot_token}/editMessageCaption"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "caption": new_caption
    }
    response = post(url, params=params)
    return response.json()

def delete_message(message_id):
    url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
    params = {
        "chat_id": chat_id,
        "message_id": message_id
    }
    response = post(url, params=params)
    return response.json()