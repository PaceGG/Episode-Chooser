from json import load
from youtube_utils import EmptyMessage
from youtube_utils import Title
from pathlib import Path
import paths

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


    def __repr__(self):
        return f"class {self.__class__.__name__}(\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())})"
        