print("Загрузка модуля database_info")
from psutil import disk_usage
import paths
from data import Data
from game import Game, select_game
from directory_statistics import *
from time_format import today, pc_date_format, short_date_format, time_format
from os import system
import telegram_utils
from console_output import borders, get_chance_color, get_strings_width, get_time__limit_color, hr

def print_info(games, stat, titles, print_flag=True):
    print(select_game(games, stat, make_selection=False))
    info = get_info(games, stat, select_game(games, stat, make_selection=False), titles)
    pc_info = info["pc"]
    system("cls")
    if print_flag: print(pc_info)

    tg_info = info["tg"]
    telegram_utils.edit_message(tg_info)

def get_info(games: list[Game], stat: Data, is_select_forced, titles):
    pc_info = ""
    tg_info = ""

    pc_info += disk_info(games, titles) + "\n"

    process_game_info = get_process_game_info(games, stat)
    tg_info += f"{process_game_info}\n\n"

    sr_info = get_snowrunner_info(stat, games[2])
    pc_info += sr_info["pc"] + "\n"
    tg_info += sr_info["tg"] + "\n\n"

    chacnes_info = get_chance_info(games, stat, is_select_forced)
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
    video_space_count = int(free_space//20)
    info_str += f"{free_space:.2f} GB ~ {video_space_count} видео\n"

    disk_video = get_disk_video(games)
    del_video = disk_video - len(titles)
    if disk_video > 0 or del_video > 0:
        info_str += f"Видео на диске: {disk_video}"
    if del_video > 0:
        info_str += f"/{del_video} из них к удалению"
    if disk_video > 0 or del_video > 0:
        info_str += "\n"

    width = get_strings_width(info_str)
    if video_space_count <= 4:
        info_str = hr("! Недостаточно места !".upper(), width=width, color="#ff0000") + info_str
    elif video_space_count <= 8:
        info_str = hr("Мало места".upper(), width=width, color="#fdca2d") + info_str
    else:
        info_str = hr("Место на диске".upper(), width=width) + info_str

    if del_video > 0:
        info_str += hr("Удалите видео".upper(), width=width, color="#ff0000")
    elif disk_video > 0:
        info_str += hr("ЗАГРУЗИТЕ ВИДЕО", width=width, color="#0078D7")

    return info_str

def get_process_game_info(games: list[Game], stat: Data):
    if stat.process_game_id == -1:
        return ""

    process_game: Game = games[stat.process_game_id]

    return f"• {process_game.full_name}... {time_format(process_game.time_limit)} [{process_game.content_time_format()}]"



def get_snowrunner_info(stat: Data, sr_game: Game):
    count_sr_session = stat.count_sr_session
    count_sr_date = stat.count_sr_date

    pc_info = ""
    tg_info = ""

    suffix = 'я' if abs(count_sr_session) == 1 else ('и' if 1 < abs(count_sr_session) < 5 else 'й')

    if count_sr_session <= 0 and count_sr_date <= today():
        pc_info += f"Сегодня SnowRunner: {time_format(sr_game.time_limit)}\n"
        tg_info += f"• Сегодня SnowRunner!!! {time_format(sr_game.time_limit)}\n"
    else:
        if count_sr_session > 0:
            pc_info += f"До SnowRunner'а ещё {count_sr_session} сесси{suffix}\n"
            tg_info += f"• SR: {count_sr_session}"
        if count_sr_date > today():
            pc_info += f"SnowRunner после {pc_date_format(count_sr_date)}\n"
            tg_info += f"• SR: {short_date_format(count_sr_date)}\n"

    pc_info = borders(pc_info, "SnowRunner", sr_game.color)

    return {"pc": pc_info, "tg": tg_info}

def get_chance_info(games: list[Game], stat: Data, is_select_forced):
    selected_game = next((game for game in games if game.is_selected), None)

    pc_info = ""
    tg_info = ""

    if is_select_forced:
        selected_game = select_game(games, stat, make_selection=False)
        pc_info += f"{selected_game.full_name}\n"
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

    if is_select_forced:
        border_color = "#ff0000"
        border_text = "FORCE"
    else:
        border_color = get_chance_color(games)
        border_text = "ШАНС"
    pc_info = borders(pc_info, border_text=border_text, color=border_color)

    return {"pc": pc_info, "tg": tg_info}

def get_time_limit_info(games: list[Game]):
    pc_info = ""

    for game in games:
        if game.time_limit != 120:
            pc_info += f"{game.full_name}: ::({time_format(game.time_limit)})::\n"
    
    pc_info = borders(pc_info, border_text="ВРЕМЯ", color=get_time__limit_color(games))

    return pc_info

def get_content_time_info(games: list[Game]):
    pc_info = ""
    for game in games:
        if game.content_time != 0:
            pc_info += f"{game.full_name}: [{game.content_time_format()}]\n"

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