from time import time
import os
from dotenv import load_dotenv
load_dotenv("gitignore/.env")

print("Загрузка модуля googleapiclient.discovery для YT...")
from googleapiclient.discovery import build
print("Загрузка модуля telegramFunctions для YT...")
from telegramFunctions import edit_telegram_caption
print("Загрузка модуля pydata для YT...")
from pydata import pydata_load, pydata_save

def intc(s):
    n = ""
    for c in s:
        if c.isdigit():
            n += c

    return n

def get_last_videos():
    print("Загрузка последних видео...")
    api_key = os.getenv("YT_API_KEY")
    channel_id = "UC2Y71nJHtoLzY88Wrrqm7Kw"

    youtube = build('youtube', 'v3', developerKey=api_key)

    channels_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    
    playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=25
    )

    try:
        playlist_response = playlist_request.execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    videos = {}

    for item in playlist_response['items']:
        try: name, number, game = item['snippet']['title'].split(" • ")
        except: continue

        number = intc(number)

        try: videos[game][number] = name
        except: videos[game] = {number: name}

    return videos

def edit_game_message(game_name, ep_range, id, last_videos):
    if game_name not in last_videos: return False
    videos = last_videos[game_name]
    names = []

    for n in range(ep_range[0],ep_range[1] +1):
        n = str(n)
        if n in videos.keys():
            names.append(videos[n])

    if len(names) != ep_range[1]-ep_range[0]+1: return False

    names_message = ""
    for name in names:
        names_message += f"• {name}\n"

    if names:
        pydata = pydata_load()
        new_text = f"{game_name} № {ep_range[0]}-{ep_range[0]+len(names)-1}: \n{names_message}"
        if len(names) == 1: new_text = f"{game_name} № {ep_range[0]}: \n{names_message}"
        try:
            if pydata["episodes_log"][game_name][1]-2 == ep_range[0] and pydata["episodes_log"][game_name][1] != ep_range[0]+len(names)-1 and "SnowRunner" not in game_name:
                pydata["episodes_log"][game_name][1] = ep_range[0]+len(names)-1
                pydata_save(pydata)
        except: pass

        edit_telegram_caption(new_text, message_id=id)
        return True
    
    return False


def edit_empty_messages():
    pydata = pydata_load()
    empty_messages = pydata_load("YT")
    if int(time()) - pydata["last_update"] < 12*60*60 and __name__ != "__main__": return
    print()
    print("Синхронизация Telegram с YouTube...")
    last_videos = get_last_videos()
    update_empty_messages = []

    for game_info in empty_messages:
        print(f"Обработка {game_info['game_name']}...")
        if not edit_game_message(game_info["game_name"], [game_info["ep_range"][0], game_info["ep_range"][1]], game_info["id"], last_videos):
            update_empty_messages.append(game_info)
            
    pydata = pydata_load()
    pydata["last_update"] = int(time())

    pydata_save(pydata)
    pydata_save(update_empty_messages, "YT")

def add_empty_message(game_name, ep_range, id):
    empty_messages = pydata_load("YT")

    empty_messages.append({"game_name": game_name, "ep_range": ep_range, "id": id})

    pydata_save(empty_messages, "YT")

def get_last_object(game_name):
    empty_messages = pydata_load("YT")

    for i in range(len(empty_messages) - 1, -1, -1):
        if game_name in empty_messages[i]["game_name"]: return empty_messages[i], i
    
    return None, None


if __name__ == '__main__':
    last_videos = get_last_videos()
    print(last_videos)

    edit_empty_messages()
    pass