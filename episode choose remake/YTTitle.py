from jsonLoader import *

yt_title_log_path = "episode choose remake/game_log_YTtitle.json"

def yt_title_pop():
    yt_log = json_load(yt_title_log_path)
    try: pop = yt_log.pop(0)
    except: pop = None
    json_save(yt_title_log_path, yt_log)

    return pop
