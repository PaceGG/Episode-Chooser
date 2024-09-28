print("Загрузка модуля episodesManipulate для classGame...")
from episodesManipulate import get_episodes, get_time
print("Загрузка модуля createGameStructure для classGame...")
from createGameStructure import create_game_structure, icon_rename, header_rename
print("Загрузка модуля timeFormat для classGame...")
from timeFormat import time_format, short_date_format
print("Загрузка модуля gameTime для classGame...")
from gameTime import calc_game_time

import PATHS
import os

def get_short_name(name):
    local = {
        "Return to Castle Wolfenstein": "Wolfenstein",
    }

    if name in local: return local[name]

    short_name = ""
    break_chars = [":", "["]
    for c in name:
        if c in break_chars or c.isnumeric(): break
        short_name += c
    name = short_name[:-1] if short_name[-1]==" " else short_name

    short_name = []
    break_words = ["Remastered"]
    for s in name.split(" "):
        if s in break_words: break
        short_name.append(s)
    name = " ".join(short_name)

    return name

class Game:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.extra_name = kwargs.get("extra_name", "")
        print(f"Инициализация {self.name}...")

        self.path = kwargs.get("path", "")
        
        safe_name = self.name.replace(":", "")

        # takes from name
        self.short_name = kwargs.get("short_name", get_short_name(self.name))

        video = kwargs.get("video", safe_name)
        self.video = os.path.join(PATHS.video, video)
        self.icon = icon_rename(safe_name)
        self.header = header_rename(safe_name)

        last_session, last_episode = get_episodes(self.name)
        self.last_session = kwargs.get("last_session", last_session)
        self.last_episode = kwargs.get("last_episode", last_episode)

        self.time = get_time(self.name)
        self.time_format = time_format(self.time)
        if self.name != "SnowRunner": self.long_time_format = f"::({time_format(self.time/3) + " / "}{time_format(self.time/2) + " / "}{time_format(self.time)})::"
        else: self.long_time_format = f"::({time_format(self.time)})::"

        self.game_time = calc_game_time(self.video)

        if self.name != "SnowRunner": self.caption = kwargs.get("caption", f"{self.extra_name} № {self.last_episode+1}-{self.last_episode+3}")
        if self.name == "SnowRunner": self.caption = kwargs.get("caption", f"{self.extra_name} № {self.last_episode+1}")

        self.date = create_game_structure(safe_name)
        self.date_format = short_date_format(self.date)

        self.chance = kwargs.get("chance", 0)

    def update_time(self):
        self.time = get_time(self.name)
        self.time_format = time_format(self.time)
        if self.name != "SnowRunner": self.long_time_format = f"::({time_format(self.time/3) + " / "}{time_format(self.time/2) + " / "}{time_format(self.time)})::"
        else: self.long_time_format = f"::({time_format(self.time)})::"
            

    def __repr__(self):
        return f"class Game:\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())}"
    
    def __getattribute__(self, item):
        if item == "extra_name":
            name = super().__getattribute__("name")
            extra_name = super().__getattribute__("extra_name")
            if extra_name == "": return name
            return f"{name}: {extra_name}"
        return super().__getattribute__(item)

if __name__ == "__main__":
    # print(get_short_name("Mafia II: Definitive Edition"))

    # test = Game(name="VLADiK BRUTAL")
    # print(test)

    # a = Game(name="Fallout: New Vegas")
    # a.extra_name = "test"

    # # print(a)

    # print(a.name)

    # print(f"{get_short_name("BioShock Remastered")}|")
    # print(f"{get_short_name("BioShock 2 Remastered")}|")

    pass