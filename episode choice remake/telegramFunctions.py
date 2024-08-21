import requests

# Инициализация бота
bot_token = token='6739691945:AAG_FoagOmFd-GUFpFwriEeTFgma-rwjGx8'
chat_id = '-1002035302407'

def send_image(image_path, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    params = {'chat_id': chat_id, 'caption': caption}
    response = requests.post(url, files=files, data=params)
    return response.json

# pinned info message id = 396
def edit_telegram_message(new_text, message_id=396):
    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text
    }
    response = requests.post(url, params=params)
    return response.json()

if __name__ == '__main__':
    send_image(r"D:\Program Files\Shadow Play\Dead Space 3\previews\1.jpg")