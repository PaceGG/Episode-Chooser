import console_setup as _
from game import *
from data import Data
import paths
from youtube_utils import EmptyMessage
from youtube_utils import edit_empty_messages
from os import startfile, chdir
from pathlib import Path
import json
from directory_statistics import get_duration
import database_info
from game import *
from os import startfile
from console_output import color_hex

chdir(paths.project_dir)

class Main:
    def __init__(self):
        # games initialization
        print("Инициализация игр")
        self.games = [Game(name=game_name) for game_name in paths.game_names[:2]]
        self.games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

        print("Инициализация данных")
        self.stat = Data("stat")
        self.empty_messages: list[EmptyMessage] = Data("empty_messages").empty_messages
        self.titles = Data("titles").titles

        edit_empty_messages(self.empty_messages, self.stat)

        # if game is new
        new_game(self.games[:2], self.stat)

        # chance calculate
        chance_calculate(self.games, self.stat.process_game_id, self.stat.queue)

        self.save_data()
        set_eng_layout()

        # info
        self.print_info()


    def launch(self):
        force_game_id = ""
        if self.stat.process_game_id == -1 and not select_game(self.games, self.stat, make_selection=False):
            force_game_id = input("Spin roulette or enter game id: ")

        if force_game_id != "":
            self.games[int(force_game_id)].is_selected = True

        # select game
        if self.stat.process_game_id == -1:
            select_game(self.games, self.stat)
        if sum(1 for game in self.games if game.is_selected) > 1:
            raise Exception("More than one game is selected")

        self.save_data()

        # run random game
        response = None
        is_last_session = False
        if self.stat.process_game_id == -1:
            response = run_game(self.games, self.stat) # no processing game
        else:
            durations = get_duration()
            duration = sum(durations) // 60
            if duration < self.games[self.stat.process_game_id].time_limit: 
                response, is_last_session = unfinished_process(self.games, self.stat, duration) # processing game

        if response is None:
            finished_process(self.games, self.stat, self.empty_messages, self.titles, is_last_session, durations) # finish processing game

        self.save_data()
        clear_selection(self.games)
        self.print_info(print_flag=False)

        if isinstance(response, Path):
            try:
                startfile(response)
            except:
                pass

        if response == "queue":
            self.launch_queue()

    def launch_queue(self):
        self.print_info()
        if self.stat.process_game_id == -1:
            print("Добавление игры в очередь невозможно так как отсутствует запущенная игра")
            return

        print()
        print("Добавление игры в очередь")

        queue_game_id = ""
        if not select_game(self.games, self.stat, make_selection=False, allow_queue=False, allow_new_game=False):
            queue_game_id = input("Spin roulette or enter game id: ")

        if queue_game_id == "":
            queue_game = select_game(self.games, self.stat, allow_queue=False)
        else:
            queue_game = self.games[int(queue_game_id)]
            print(f"{color_hex(queue_game.name, queue_game.color)}")
            print("Будет добавлена в очередь, продолжить?")
            input()

        self.stat.queue.append(queue_game.id)
        self.stat.add_game_log(queue_game.name)

        self.save_data()

        chance_calculate(self.games, self.stat.process_game_id, self.stat.queue)

        self.print_info(print_flag=False)
        print()
        print(f"{color_hex(queue_game.name, queue_game.color)}")
        print("Добавлена в очередь")
        input()

    def save_data(self):
        with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
            file = json.load(file)
            cache = file["cache"]
            stat_backup = file["stat_backup"]
    
        data = {}
        data["stat"] = self.stat.__dict__
        data["stat_backup"] = stat_backup
        data["game"] = [item.as_dict() for item in self.games]
        data["empty_messages"] = [item.__dict__ for item in self.empty_messages]
        data["titles"] = [item.__dict__ for item in self.titles]
        data["cache"] = cache
    
        with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def print_info(self, print_flag=True):
        database_info.print_info(self.games, self.stat, self.titles, print_flag=print_flag)
        

if __name__ == "__main__":
    main = Main()
    # main.launch_queue()
    main.launch()