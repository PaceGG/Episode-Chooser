from Game import *
from Data import Data
import PATH
from info import get_info
from youTube import EmptyMessage
import telegram
from youTube import edit_empty_messages
from os import startfile

class Main:
    def main(self):
        # games initialization
        games = [Game(name=game_name) for game_name in PATH.game_names[:2]]
        games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

        stat = Data("stat")
        empty_messages: list[EmptyMessage] = Data("empty_messages").empty_messages
        titles = Data("titles").titles

        # if game is new
        new_game(games[:2], stat)

        # chance calculate
        chance_calculate(games)

        # select game
        selected_game, is_select_forced = select_game(games, stat, skip_roulette=True)

        if sum(1 for game in games if game.is_selected) > 1:
            raise Exception("More than one game is selected")
        
            
        # info
        # info_str = get_info(games, stat, is_select_forced)
        info = get_info(games, stat, is_select_forced, titles)
        pc_info = info["pc"]
        print(pc_info)

        tg_info = info["tg"]
        telegram.edit_message(tg_info)

        # run random game
        response = None
        is_last_session = False
        if stat.process_game_id == -1:
            response = run_game(games, stat) # no processing game
        else:
            if get_duration() < games[stat.process_game_id].time_limit: 
                response, is_last_session = unfinished_process(games, stat) # processing game

        if response is None:
            finished_process(games, stat, empty_messages, titles, is_last_session) # finish processing game

        with open('data.json', 'r', encoding='utf-8') as file:
            cache = json.load(file)["cache"]

        data = {}
        data["stat"] = stat.__dict__
        data["game"] = [item.__dict__() for item in games]
        data["empty_messages"] = [item.__dict__ for item in empty_messages]
        data["titles"] = [item.__dict__ for item in titles]
        data["cache"] = cache

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        startfile(response)

        

if __name__ == "__main__":
    main = Main()
    main.main()