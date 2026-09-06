from database_info import print_info
from game import *
from os import startfile

class Launcher:
    def __init__(self, main):
        self.games = main.games
        self.stat = main.stat
        self.empty_messages = main.empty_messages
        self.titles = main.titles
        self.save_data = main.save_data


    def launch(self):
        # info
        print_info(self.games, self.stat, self.titles)

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
        print_info(self.games, self.stat, self.titles, print_flag=False)

        if response not in ["redo", "skip-run"]:
            try:
                startfile(response)
            except:
                pass
