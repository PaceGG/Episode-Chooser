from episodesManipulate import get_episodes, get_time
from createGameStructure import create_game_structure, icon_rename
from timeFormat import time_format, short_date_format
# from gameTime import calc_game_time

def get_short_name(name):
    short_name = ""
    break_chars = [":", "["]
    for c in name:
        if c in break_chars or c.isnumeric(): return short_name[:-1] if short_name[-1]==" " else short_name
        short_name += c

    return short_name

class Game:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.path = kwargs.get("path", "")
        
        safe_name = self.name.replace(":", "")

        # берем из имени
        self.short_name = kwargs.get("short_name", get_short_name(self.name))

        video = kwargs.get("video", safe_name)
        self.video = f"D:/Program Files/Shadow Play/{video}"
        self.icon = icon_rename(safe_name)

        last_session, last_episode = get_episodes(self.name)
        self.last_session = kwargs.get("last_session", last_session)
        self.last_episode = kwargs.get("last_episode", last_episode)

        self.time = get_time(self.name)
        self.time_format = time_format(self.time)
        self.long_time_format = f"::({time_format(self.time/3) + " / "}{time_format(self.time/2) + " / "}{time_format(self.time)})::"

        # self.game_time = calc_game_time(self.video)

        if self.name != "SnowRunner": self.caption = kwargs.get("caption", f"{self.name} № {self.last_episode+1}-{last_episode+3}:\n• \n• \n• ")
        elif self.name == "SnowRunner": self.caption = kwargs.get("caption", f"{self.name} № {self.last_episode+1}:\n• ")

        self.date = create_game_structure(safe_name)
        self.date_format = short_date_format(self.date)

        self.chance = kwargs.get("chance", 0)

    def update_time(self):
        self.time = get_time(self.name)
        self.time_format = time_format(self.time)
        self.long_time_format = f"::({time_format(self.time/3) + " / "}{time_format(self.time/2) + " / "}{time_format(self.time)})::"
            

    def __repr__(self):
        return f"class Game:\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())}"

if __name__ == "__main__":
    # print(get_short_name("Mafia II: Definitive Edition"))

    # test = Game(name="VLADiK BRUTAL")
    # print(test)

    # a = Game(name="Fallout: New Vegas")
    b = Game(name="VLADiK BRUTAL")

    # print(a)
    # print()
    print(b)

    pass