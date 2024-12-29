from psutil import disk_usage
import paths
from data import Data
from game import Game, check_force
from directory_statistics import *
from time_format import today, pc_date_format, short_date_format, time_format
from os import system
import telegram_utils

def print_info(games, stat, titles):
    info = get_info(games, stat, check_force(games, stat), titles)
    pc_info = info["pc"]
    system("cls")
    print(pc_info)

    tg_info = info["tg"]
    telegram_utils.edit_message(tg_info)

def get_info(games: list[Game], stat: Data, is_select_forced: bool, titles):
    pc_info = ""
    tg_info = ""

    pc_info += disk_info(games, titles) + "\n"

    sr_info = get_snowrunner_info(stat, games[2])
    pc_info += sr_info["pc"] + "\n"
    tg_info += sr_info["tg"] + "\n\n"

    chacnes_info = get_chance_info(games[:2], is_select_forced)
    pc_info += chacnes_info["pc"] + "\n"
    tg_info += chacnes_info["tg"] + "\n"

    time_limit_info = get_time_limit_info(games[:2])
    pc_info += time_limit_info + "\n"

    content_time_info = get_content_time_info(games)
    pc_info += content_time_info + "\n"

    tg_time_info = get_tg_time_info(games)
    tg_info += tg_time_info + "\n"

    tg_sr_date_info = f"• SR after {pc_date_format(stat.count_sr_date)}\n"
    tg_info += tg_sr_date_info

    next_update_info = f"• Next update: {pc_date_format(stat.last_update + 12*60*60)}\n"
    tg_info += next_update_info

    return {"pc": pc_info, "tg": tg_info}


def disk_info(games: list[Game], titles: list):
    info_str = ""

    free_space = disk_usage(str(paths.video_dir.drive)).free/1024/1024/1024
    info_str += f"Место на диске: {free_space:.2f} GB ~ {int(free_space//15)} видео\n"

    disk_video = get_disk_video(games)
    info_str += f"Видео на диске: {disk_video}\n"

    info_str += f"Видео к удалению: {disk_video - len(titles)}\n"
    return info_str

def get_snowrunner_info(stat: Data, sr_game: Game):
    count_sr_session = stat.count_sr_session
    count_sr_date = stat.count_sr_date

    pc_info = ""
    tg_info = ""

    suffix = 'я' if abs(count_sr_session) == 1 else ('и' if 1 < abs(count_sr_session) < 5 else 'й')

    if count_sr_session <= 0 and count_sr_date <= today():
        pc_info += f"Сегодня SnowRunner: {time_format(sr_game.time_limit)}\n"
        tg_info += f"• Сегодня SnowRunner!!! {time_format(sr_game.time_limit)}\n"
    elif count_sr_session > 0:
        pc_info += f"До SnowRunner'а ещё {count_sr_session} сесси{suffix}\n"
        tg_info += f"• SR: {count_sr_session}"
    else:
        pc_info += f"SnowRunner после {pc_date_format(count_sr_date)}\n"
        tg_info += f"• SR: {short_date_format(count_sr_date)}\n"

    return {"pc": pc_info, "tg": tg_info}

def get_chance_info(games: list[Game], is_select_forced):
    selected_game = next((game for game in games if game.is_selected), None)

    pc_info = ""
    tg_info = ""

    if is_select_forced:
        pc_info += f"Force: {selected_game.full_name}\n"
        tg_info += f"• Force: {selected_game.short_name}\n"
    
    if games[0].chance == games[1].chance == 1:
        pc_info += "Шансы равны\n"
        tg_info += "• Шансы равны\n"
    else:
        for game in games[:2]:
            if game.chance <= 1:
                continue
            pc_info += f"{game.full_name}: {game.chance}\n"
            tg_info += f"• {game.short_name}: {game.chance}\n"

    return {"pc": pc_info, "tg": tg_info}

def get_time_limit_info(games: list[Game]):
    pc_info = ""

    for game in games:
        if game.time_limit != 120:
            pc_info += f"{game.full_name}: ::({time_format(game.time_limit)})::\n"
    
    return pc_info

def get_content_time_info(games: list[Game]):
    pc_info = ""
    for game in games:
        if game.content_time != 0:
            pc_info += f"{game.full_name}: [{game.content_time_format()}]"

    return pc_info

def get_tg_time_info(games: list[Game]):
    tg_info = ""

    for game in games:
        if game.time_limit != 120 or game.content_time != 0:
            tg_info += f"• {game.short_name}:"
            if game.time_limit != 120:
                tg_info += f" {time_format(game.time_limit)}"
            if game.content_time != 0:
                tg_info += f" [{game.content_time_format()}]"
            tg_info += "\n"

    return tg_info
