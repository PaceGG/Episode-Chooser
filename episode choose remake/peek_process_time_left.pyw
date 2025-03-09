import json
from os import chdir
from pathlib import Path
from time import sleep

from data import Data
from directory_statistics import get_duration
from game import Game
import paths
from telegram_utils import send_message, delete_message
from time_format import time_format

def save_data(stat: Data):
    data_file_path = Path(paths.root_dir) / "data.json"

    with data_file_path.open('r+', encoding='utf-8') as file:
        data = json.load(file)
        data["stat"] = stat.__dict__
        file.seek(0)
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.truncate()


chdir(paths.project_dir)

stat = Data("stat")

if stat.time_info_message_id != -1: delete_message(stat.time_info_message_id)

if stat.process_game_id == -1:
    message_id = send_message("No process game")
    stat.time_info_message_id = message_id
    save_data(stat)
    sleep(5)
    delete_message(message_id)
    stat.time_info_message_id = -1
    save_data(stat)
    exit(0)

games = [Game(name=game_name) for game_name in paths.game_names[:2]]
games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

process_game = games[stat.process_game_id]
time_limit = process_game.time_limit
user_time = get_duration()
time_left = time_limit - user_time

if time_left >= 0: message = f"{process_game.full_name}... {time_format(time_left)} [{process_game.content_time_format()}]"
else: message = f"{process_game.full_name}... Complete!"
message_id = send_message(message)
stat.time_info_message_id = message_id

save_data(stat)