import ctypes
import os

def set_window_pos(icon_path, title, x, y, width, height):
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    hwnd = kernel32.GetConsoleWindow()

    # Позиция и размеры
    user32.MoveWindow(hwnd, x, y, width, height, True)

    # Заголовок
    user32.SetWindowTextW(hwnd, title)

    # Загружаем иконку из файла
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    hicon = user32.LoadImageW(
        0,
        icon_path,
        IMAGE_ICON,
        256,
        256,
        LR_LOADFROMFILE
    )

    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1

    # Для заголовка
    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    # Для панели задач
    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)




set_window_pos(r"..\Visual Elements\icon-square.ico", "Episode Chooser", 472, 276, 374, 444)
os.system('mode con: cols=50 lines=28')

from game import *
from data import Data
import paths
from database_info import print_info
from youtube_utils import EmptyMessage
from youtube_utils import edit_empty_messages
from os import startfile, chdir
from pathlib import Path
import json
from directory_statistics import get_duration

chdir(paths.project_dir)

def save_data(stat, games, empty_messages, titles):
    with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
        file = json.load(file)
        cache = file["cache"]
        stat_backup = file["stat_backup"]

    data = {}
    data["stat"] = stat.__dict__
    data["stat_backup"] = stat_backup
    data["game"] = [item.as_dict() for item in games]
    data["empty_messages"] = [item.__dict__ for item in empty_messages]
    data["titles"] = [item.__dict__ for item in titles]
    data["cache"] = cache

    with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class Main:
    def main(self):
        # games initialization
        print("Инициализация игр")
        games = [Game(name=game_name) for game_name in paths.game_names[:2]]
        games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

        print("Инициализация данных")
        stat = Data("stat")
        empty_messages: list[EmptyMessage] = Data("empty_messages").empty_messages
        titles = Data("titles").titles

        edit_empty_messages(empty_messages, stat)

        # if game is new
        new_game(games[:2], stat)

        # chance calculate
        chance_calculate(games)
        
        save_data(stat, games, empty_messages, titles)

        # info
        print_info(games, stat, titles)

        force_game_id = ""
        if stat.process_game_id == -1 and not select_game(games, stat, make_selection=False):
            force_game_id = input("Spin roulette or enter game id: ")

        if force_game_id != "":
            games[int(force_game_id)].is_selected = True

        # select game
        if stat.process_game_id == -1:
            select_game(games, stat)
        if sum(1 for game in games if game.is_selected) > 1:
            raise Exception("More than one game is selected")

        save_data(stat, games, empty_messages, titles)

        # run random game
        response = None
        is_last_session = False
        if stat.process_game_id == -1:
            response = run_game(games, stat) # no processing game
        else:
            durations = get_duration()
            duration = sum(durations) // 60
            if duration < games[stat.process_game_id].time_limit: 
                response, is_last_session = unfinished_process(games, stat, duration) # processing game

        if response is None:
            finished_process(games, stat, empty_messages, titles, is_last_session, durations) # finish processing game

        save_data(stat, games, empty_messages, titles)
        clear_selection(games)
        print_info(games, stat, titles, print_flag=False)

        if response != "redo":
            try:
                startfile(response)
            except:
                print(f"Ярлык с игрой не найден.")

        

if __name__ == "__main__":
    main = Main()
    main.main()