import json
from time import time

from googleapiclient.discovery import build
from telegramFunctions import *
from pydata import pydata_load, pydata_save

with open("episode choice remake/YT.json", encoding="utf-8") as f:
    empty_messages = json.load(f)

def search_videos_on_channel(search_string, type="video"):
    api_key = 'AIzaSyCTcKHZ4w2LNlG_KX7p-2UxFd_VPlE_jJQ'
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
    videos = search_videos_on_channel(game_name if game_name != "SnowRunner" else "SnowRunner [ng+]")
    names = []

    for n in range(ep_range[0],ep_range[1] +1):
        if n in videos.keys():
            names.append(videos[n])

    names_message = ""
    for name in names:
        names_message += f"• {name}\n"

    pydata = pydata_load()
    if names:
        new_text = f"{game_name} № {ep_range[0]}-{ep_range[0]+len(names)-1}: \n{names_message}"
        if game_name == "SnowRunner": new_text = f"{game_name} № {ep_range[0]}: \n{names_message}"
        if pydata["episodes_log"][game_name][1]-2 == ep_range[0] and pydata["episodes_log"][game_name][1] != ep_range[0]+len(names)-1 and game_name != "SnowRunner":
            pydata["episodes_log"][game_name][1] = ep_range[0]+len(names)-1
            pydata_save(pydata)

        edit_telegram_caption(new_text, message_id=id)
        return True
    
    return False



def edit_empty_messages():
    pydata = pydata_load()
    if int(time()) - pydata["last_update"] < 12*60*60: return
    update_empty_messages = []

    for game_info in empty_messages:
        if not edit_game_message(game_info["game_name"], game_info["ep_range"], game_info["id"]):
            update_empty_messages.append(game_info)

    with open("episode choice remake/YT.json", "w", encoding="utf-8") as f:
        json.dump(update_empty_messages, f, indent=4)

    pydata["last_update"] = int(time())
    pydata_save(pydata)

def add_empty_message(game_name, ep_range, id):
    empty_messages.append({"game_name": game_name, "ep_range": ep_range, "id": id})

    with open("episode choice remake/YT.json", "w", encoding="utf-8") as f:
        json.dump(empty_messages, f, indent=4)


if __name__ == '__main__':
    # edit_game_message("Dead Space 3", [4,5], 462)
    edit_empty_messages()
    pass