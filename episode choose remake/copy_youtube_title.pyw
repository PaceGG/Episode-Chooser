from pyautogui import hotkey
from pyperclip import copy
from util import set_eng_layout
from pathlib import Path

from data import Data
import json

titles = Data("titles").titles

if len(titles) == 0:
    exit()

with open(Path.joinpath(Path(__file__).resolve().parent, 'data.json'), 'r', encoding='utf-8') as file:
    data = json.load(file)

set_eng_layout()
copy(titles[0])
hotkey('ctrl', 'v')

data["titles"] = [item.__dict__ for item in titles if item.episode != -2]

with open(Path.joinpath(Path(__file__).resolve().parent, 'data.json'), 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)