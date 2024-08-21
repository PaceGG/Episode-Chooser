from episodesManipulate import *
from createGameStructure import *
from math import ceil
from time import strftime, localtime

def get_short_name(name):
    short_name = ""
    break_chars = [":", "["]
    for c in name:
        if c in break_chars or c.isnumeric(): return short_name[:-1] if short_name[-1]==" " else short_name
        short_name += c

    return short_name
def time_format(minutes):
    minutes = ceil(minutes)
    if minutes > 60: return f"{minutes//60:02}:{minutes%60:02} ({minutes})"
    return str(ceil(minutes))
class Game:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.path = kwargs.get("path", "")
        
        safe_name = self.name.replace(":", "")

        # берем из имени
        self.short_name = kwargs.get("short_name", get_short_name(self.name))
        video = kwargs.get("video", safe_name)
        self.video = f"D:/Program Files/Shadow Play/{video}/previews"
        self.icon = kwargs.get("icon", f"D:/Program Files/HTML/Games/icons_new/{safe_name}.png")

        last_session, last_episode = get_episodes(self.name)
        self.last_session = kwargs.get("last_session", last_session)
        self.last_episode = kwargs.get("last_episode", last_episode)

        self.time = get_time(self.name)
        self.time_format = time_format(self.time)
        self.long_time_format = f"::({time_format(self.time/3) + " / "}{time_format(self.time/2) + " / "}{time_format(self.time)})::"

        if self.name != "SnowRunner": self.caption = kwargs.get("caption", f"{self.name} № {self.last_episode+1}-{last_episode+3}:\n• \n• \n• ")
        elif self.name == "SnowRunner": self.caption = kwargs.get("caption", f"{self.name} № {self.last_episode+1}:\n• ")

        self.date = create_game_structure(safe_name)
        self.date_format = strftime("%d.%m.%y %H:%M", localtime(self.date))

        self.chance = kwargs.get("chance", 0)
            

    def __repr__(self):
        return f"class Game:\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())}"
    
    # Недоделано и нигде не используется
    # def set_name(self, name):
    #     self.name = name
    #     self.short_name = get_short_name(self.name)
    #     self.video = self.name.replace(":", "")
    #     self.video = f"D:/Program Files/Shadow Play/{name.replace(":", "")}/previews"

if __name__ == "__main__":
    # print(get_short_name("Mafia II: Definitive Edition"))

    test = Game(name="Dead Space 4")
    print(test)

    pass