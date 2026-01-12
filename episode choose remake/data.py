print("Загрузка модуля data")
from json import dump, load
from youtube_utils import EmptyMessage
from youtube_utils import Title
from pathlib import Path
import paths
from telegram_utils import delete_message

class Data:
    games_list: list[str]
    count_sr_session: int
    count_sr_date: int
    durations: dict
    games_log: list
    process_game_id: int
    process_game_message_id: int
    empty_messages: list[EmptyMessage]
    titles: list[Title]
    last_update: int
    time_info_message_id: int

    def __init__(self, data_type):
        with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
            data = load(file)[data_type]

        if type(data) == dict:
            for key, value in data.items():
                setattr(self, key, value)
        if type(data) == list and data_type == "empty_messages":
            empty_messages = []
            for item in data:
                empty_messages.append(EmptyMessage(**item))
            self.empty_messages = empty_messages
        if type(data) == list and data_type == "titles":
            titles = []
            for item in data:
                titles.append(Title(**item))
            self.titles = titles

    def add_game_log(self, game_name: str):
        self.games_log = self.games_log[1:] + [game_name]

    def make_backup(self):
        with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
            data = load(file)
        
        data["stat_backup"] = data["stat"]        

        with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
            dump(data, file)

    def restore_backup(self):
        backup = Data("stat_backup")
        if self.process_game_message_id != -1:
            delete_message(self.process_game_message_id)
        if self.time_info_message_id != -1:
            delete_message(self.time_info_message_id)
        for k, v in vars(backup).items():
            setattr(self, k, v)


    def __repr__(self):
        return f"class {self.__class__.__name__}(\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())})"
        