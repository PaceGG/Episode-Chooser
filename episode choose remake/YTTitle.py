from jsonLoader import *

yt_title_log_path = "episode choose remake/game_log_YTtitle.json"

def yt_title_pop():
    yt_log = json_load(yt_title_log_path)
    try: pop = yt_log.pop(0)
    except: pop = None
    json_save(yt_title_log_path, yt_log)

    return pop

def add_yt_titles(game_name):
    from episodesManipulate import get_last_object
    yt_log = json_load(yt_title_log_path)
    ep_range = get_last_object(game_name)[0]["ep_range"]

    for i in range(ep_range[0], ep_range[1] +1):
        yt_log.append(f" • № {i} • {game_name}")
        if i == 1: yt_log.append(game_name)

    json_save(yt_title_log_path, yt_log)