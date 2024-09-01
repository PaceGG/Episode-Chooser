from time import time
from dotenv import load_dotenv
import os
load_dotenv()

print("Загрузка модуля googleapiclient.discovery для YT...")
from googleapiclient.discovery import build
print("Загрузка модуля telegramFunctions для YT...")
from telegramFunctions import edit_telegram_caption
print("Загрузка модуля pydata для YT...")
from pydata import pydata_load, pydata_save
print("Загрузка модуля jsonLoader для YT...")
from jsonLoader import *
empty_messages_path = "episode choice remake/YT.json"

shift_range = {}

def search_videos_on_channel(search_string, type="video"):
    api_key = os.getenv("YT_API_KEY")
    channel_id = "UC2Y71nJHtoLzY88Wrrqm7Kw"

    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=25,
        order='date',
        type=type
    )

    try:
        response = request.execute()
    except:
        return {}

    videos = {}
    for item in response['items']:
        video_title = item['snippet']['title']
        if search_string.lower() in video_title.lower():
            videos[int(video_title.split(" • ")[1][2:])] = video_title.split(" • ")[0]

    return videos

def edit_game_message(game_name, ep_range, id):
    global shift_range
    videos = search_videos_on_channel(game_name if game_name != "SnowRunner" else "SnowRunner [ng+]")
    names = []

    for n in range(ep_range[0],ep_range[1] +1):
        if n in videos.keys():
            names.append(videos[n])

    names_message = ""
    for name in names:
        names_message += f"• {name}\n"

    if names:
        pydata = pydata_load()
        new_text = f"{game_name} № {ep_range[0]}-{ep_range[0]+len(names)-1}: \n{names_message}"
        if len(names) == 1: new_text = f"{game_name} № {ep_range[0]}: \n{names_message}"
        if pydata["episodes_log"][game_name][1]-2 == ep_range[0] and pydata["episodes_log"][game_name][1] != ep_range[0]+len(names)-1 and game_name != "SnowRunner":
            pydata["episodes_log"][game_name][1] = ep_range[0]+len(names)-1

            pydata_save(pydata)

        try: shift_range[game_name] += 3-len(names)
        except: shift_range[game_name] = 3-len(names)

        edit_telegram_caption(new_text, message_id=id)
        return True
    
    return False


def edit_empty_messages():
    pydata = pydata_load()
    empty_messages = json_load(empty_messages_path)
    # if int(time()) - pydata["last_update"] < 12*60*60: return
    print()
    print("Синхронизация Telegram с YouTube...")
    update_empty_messages = []

    for game_info in empty_messages:
        try: s_range = shift_range[game_info["game_name"]]
        except: s_range = 0
        if not edit_game_message(game_info["game_name"], [game_info["ep_range"][0]-s_range, game_info["ep_range"][1]-s_range], game_info["id"]):
            update_game_info = game_info
            update_game_info["ep_range"][0] -= s_range
            update_game_info["ep_range"][1] -= s_range
            update_empty_messages.append(update_game_info)
            
    pydata = pydata_load()
    pydata["last_update"] = int(time())
    


    if shift_range != {}:
        for game_info in update_empty_messages:
            pydata["episodes_log"][game_info["game_name"]][1] = game_info["ep_range"][1]
            edit_telegram_caption(f"{game_info["game_name"]} № {f"{game_info["ep_range"][0]}-{game_info["ep_range"][1]}" if game_info["ep_range"][0] != game_info["ep_range"][1] else game_info['ep_range'][0]}:", message_id=game_info["id"])

    pydata_save(pydata)
    json_save(empty_messages_path, update_empty_messages)

def add_empty_message(game_name, ep_range, id):
    empty_messages = json_load(empty_messages_path)

    empty_messages.append({"game_name": game_name, "ep_range": ep_range, "id": id})

    json_save(empty_messages_path, empty_messages)


if __name__ == '__main__':
    # edit_game_message("Dead Space 3", [4,5], 462)
    # edit_empty_messages()

    

    pass