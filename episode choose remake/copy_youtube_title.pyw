from pyautogui import hotkey
from pyperclip import copy
from util import set_eng_layout
from pathlib import Path
from data import Data
import json
import paths
from time_format import today, get_minute

titles = Data("titles").titles

if len(titles) == 0:
    exit()

with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

stat = Data("stat")
last_title_time = stat.last_title_time
current_time = max(today(), last_title_time)

if get_minute(last_title_time) == get_minute(current_time) and current_time - last_title_time <= 60:
    current_time += 60

title = titles[0].get_title(current_time)

if "•" not in title: stat.last_title_time = current_time

data["titles"] = [item.__dict__ for item in titles if item.episode != -2]
data["stat"] = stat.__dict__

with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

set_eng_layout()
copy(title)
hotkey('ctrl', 'v')
print(title)