from game import *
from data import Data
import paths
from database_info import print_info
from youtube_utils import EmptyMessage
import telegram_utils
from youtube_utils import edit_empty_messages
from os import startfile, chdir, system
from pathlib import Path
import json
from directory_statistics import get_duration

chdir(paths.project_dir)

def save_data(stat, games, empty_messages, titles):
    with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
        cache = json.load(file)["cache"]

    data = {}
    data["stat"] = stat.__dict__
    data["game"] = [item.__dict__() for item in games]
    data["empty_messages"] = [item.__dict__ for item in empty_messages]
    data["titles"] = [item.__dict__ for item in titles]
    data["cache"] = cache

    with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class Main:
    def main(self):
        # games initialization
        games = [Game(name=game_name) for game_name in paths.game_names[:2]]
        games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

        stat = Data("stat")
        empty_messages: list[EmptyMessage] = Data("empty_messages").empty_messages
        titles = Data("titles").titles

        edit_empty_messages(empty_messages, stat)

        # if game is new
        new_game(games[:2], stat)

        # chance calculate
        chance_calculate(games)

        # info
        print_info(games, stat, titles)
        if stat.process_game_id == -1:
            force_game_id = input()
        else:
            force_game_id = ""
        if force_game_id != "":
            games[force_game_id].is_selected = True

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
            duration = get_duration()
            if duration < games[stat.process_game_id].time_limit: 
                response, is_last_session = unfinished_process(games, stat, duration) # processing game

        if response is None:
            finished_process(games, stat, empty_messages, titles, is_last_session, duration) # finish processing game

        save_data(stat, games, empty_messages, titles)
        clear_selection(games)
        print_info(games, stat, titles)

        if response:
            startfile(response)

        

if __name__ == "__main__":
    main = Main()
    main.main()