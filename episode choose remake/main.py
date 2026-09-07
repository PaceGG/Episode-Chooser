import console_setup
from game import *
from data import Data
import paths
from youtube_utils import EmptyMessage
from youtube_utils import edit_empty_messages
from os import startfile, chdir
from pathlib import Path
import json
from directory_statistics import get_duration
from launcher import Launcher
from game import GamesManager
from ec_collections.data_collection import DataManager

chdir(paths.project_dir)

class Main:
    def __init__(self):
        # games initialization
        self.games = GamesManager()
        self.data = DataManager()

        self.data.edit_empty_messages()

        # if game is new
        new_game(self.games[:2], self.stat)

        # chance calculate
        chance_calculate(self.games)

        self.save_data()
        set_eng_layout()

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
        

if __name__ == "__main__":
    main = Main()
    launcher = Launcher(main)
    launcher.launch()