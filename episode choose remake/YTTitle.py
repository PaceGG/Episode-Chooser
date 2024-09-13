import json
import PATHS

from pydata import *
from timeFormat import get_time

def yt_title_pop():
    yt_log = pydata_load("game_log_YTTitle")

    return_str = yt_log[0]

    if "•" in return_str:
        yt_log[0] = get_time()
        pydata_save(yt_log, "game_log_YTTitle")
        return return_str
    else:
        try: pop = yt_log.pop(0)
        except: pop = None
        pydata_save(yt_log, "game_log_YTTitle")
        return pop

def add_yt_titles(game_name, number_of_videos=3):
    from episodesManipulate import get_last_object

    with open("react-remake/db.json", encoding="utf-8") as f:
        showcase = json.load(f)["showcase"]

    extra_name = ""
    if game_name == "SnowRunner":
        extra_name = PATHS.extra_names[2]
    else:
        for item in showcase:
            if item["name"] == game_name:
                extra_name = PATHS.extra_names[int(item["id"])]

    if extra_name != "": game_name = f"{game_name}: {extra_name}"

    yt_log = pydata_load("game_log_YTTitle")
    ep_range = get_last_object(game_name)[0]["ep_range"]
    ep_range[1] -= 3 - number_of_videos

    for i in range(ep_range[0], ep_range[1] +1):
        yt_log.append(f"• № {i} • {game_name}")
        if i == 1: yt_log.append(game_name)

    pydata_save(yt_log, "game_log_YTTitle")