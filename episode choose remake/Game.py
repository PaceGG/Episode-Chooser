import paths
import json
from pathlib import Path
from time_format import time_format, today
from data import Data
from roulette import spin_roulette
from util import *
from youtube_utils import add_titles, add_empty_message
from directory_statistics import *

def get_short_name(name):
    local = {
        "Return to Castle Wolfenstein": "Wolfenstein",
        "Far Cry Primal": "Far Cry",
        "SnowRunner [ng+]": "SR"
    }

    if name in local: return local[name]

    s = ""
    break_chars = {':', '['}
    for c in name:
        c: str
        if c in break_chars or c.isnumeric(): break
        s += c
    name = s.strip()

    l = []
    break_words = ["Remastered"]
    for s in name.split(" "):
        if s in break_words: break
        l.append(s)
    if len(l) <= 2:
        name = " ".join(l)
    else:
        name = "".join([s[0] for s in l])

    return name

class Game:
    def __init__(self, name: str, **kwargs):
        try:
            self.id = paths.game_names.index(name)
        except ValueError:
            raise ValueError(f"Unknown game: {name}")
                
        self.name = name
        self.safe_name = kwargs.get("safe_name", name.replace(':', ''))
        self.short_name = get_short_name(name)
        self.extra_name = paths.extra_names[self.id]
        self.full_name = f"{self.name}{f": {self.extra_name}" if self.extra_name else ''}"

        self.color = paths.game_colors[self.id]

        self.game_path = paths.game_paths[self.id]
        self.video_dir = paths.joinpath(paths.video_dir, self.safe_name)
        if not self.video_dir.exists(): create_game_folder(self.video_dir)

        stat = Data("stat")
        with open(Path.joinpath(Path(__file__).resolve().parent, 'data.json'), 'r', encoding='utf-8') as file:
            if self.name not in stat.games_list and self.id != 2:
                game_data = {
                    "name": self.name,
                    "count_session": 0,
                    "count_episode": 0,
                    "time_limit": 120,
                    "content_time": 0,
                    "user_time": 0,
                    "is_complete": False
                }
                self.is_game_new = True
            else:
                game_data = json.load(file)["game"][self.id]
                self.is_game_new = False
    
        self.count_session = game_data["count_session"]
        self.count_episode = game_data["count_episode"]
        self.time_limit = game_data["time_limit"]
        self.content_time = game_data["content_time"]
        self.user_time = game_data["user_time"]

        self.chance = 1
        self.is_selected = False

        self.caption = f"{self.full_name}..."
        self.header = Path.joinpath(paths.video_dir, "headers", self.safe_name + ".png")
        if not self.header.exists(): header_rename(self.safe_name)

    def content_time_format(self):
        return f"{"+" if self.content_time > 0 else ""}{self.content_time}"

    def __repr__(self):
        return f"class {self.__class__.__name__}(\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())})"
    
    def __dict__(self):
        return {
            "name": self.name,
            "count_session": self.count_session,
            "count_episode": self.count_episode,
            "time_limit": self.time_limit,
            "content_time": self.content_time,
            "user_time": self.user_time
        }
    
    
def chance_calculate(games: list[Game]):
    min(games[:2], key=lambda game: game.count_session).chance += abs(games[0].count_session - games[1].count_session)
    games[2].chance = 0

def new_game(games: list[Game], stat: Data):
    for game in games[:2]:
        if game.is_game_new:
                stat.games_list[game.id] = game.name

                games[(not game.id)].count_session = 0
                if stat.count_sr_session < 5: stat.count_sr_session = 5

                game.is_selected = True
                game.is_game_new = False

def get_selected_game(games: list[Game]):
    return next((game for game in games if game.is_selected), None)

def clear_selection(games: list[Game]):
    for game in games:
        game.is_selected = False

def select_game(games: list[Game], stat: Data, skip_roulette = False):
    # force new game (not in game list)
    selected_game = next((game for game in games[:2] if game.is_selected), None)
    if selected_game is not None:
        return selected_game, True

    # force new game (sessions == 0)
    if games[0].count_session == games[1].count_session == 0:
        selected_game = max(games[:2], key=lambda game: game.video_dir.stat().st_birthtime)
        selected_game.is_selected = True
        return selected_game, True
    
    # force sr
    if stat.count_sr_session <= 0 and stat.count_sr_date <= today():
        games[2].is_selected = True
        return selected_game, False

    # force unpopular game (games_log)
    if len(set(stat.games_log)) == 1:
        unpopular_game = next((game for game in games[:2] if game.name in stat.games_log), None)
        if unpopular_game is not None:
            unpopular_game.is_selected = True
            return unpopular_game, True

    # no force
    selected_game = spin_roulette(games, skip=skip_roulette)
    selected_game.is_selected = True
    return selected_game, False

def run_game(games: list[Game], stat: Data):
    import telegram_utils
    set_eng_layout()
    selected_game = get_selected_game(games)

    confirm = input()

    print(f"{selected_game.full_name}{f" {time_format(selected_game.time_limit)}" if selected_game.time_limit != 120 else ''}")
    stat.process_game_message_id = telegram_utils.send_image(selected_game.header, selected_game.caption)

    
    if selected_game.id != 2:
        stat.add_game_log(selected_game.name)
        stat.count_sr_session -= 1
    else:
        stat.count_sr_session += 5
        stat.count_sr_date = today() + 7*24*60*60

    selected_game.count_session += 1
    chance_calculate(games)

    stat.process_game_id = selected_game.id

    return selected_game.game_path


def unfinished_process(games: list[Game], stat: Data):
    unfinished_game = games[stat.process_game_id]
    duration = get_duration()

    # склонение существительного
    if duration % 10 == 1 and duration % 100 != 11: form = "минута"
    elif duration % 10 in {2, 3, 4} and not (duration % 100 in {12, 13, 14}): form = "минуты"
    else: form = "минут"

    print(f"Сессия {unfinished_game.name} ещё не завершена, осталось {unfinished_game.time_limit - duration} {form}")
    print(f"Запустить {unfinished_game.name}? Введите \"-\" для обозначения финальной сессии")
    confirm = input()
    if confirm == "-": return None, True
    return unfinished_game.game_path, False

def finished_process(games: list[Game], stat: Data, empty_messages, titles, is_last_session): 
    import telegram_utils
    process_game_id = stat.process_game_id
    message_id = stat.process_game_message_id
    processed_game = games[process_game_id]

    duration = get_duration() if not(is_last_session) else 120
    count_videos = get_count_videos()

    print(f"В {processed_game.name} есть видео продолжительностью {duration} минут. Добавить их к сумме?")
    user_time = input(f"Введите время для {processed_game.name}: ")
    if user_time == "": user_time = duration
    else: user_time = int(user_time)
    processed_game.user_time = user_time
    equalize_time_limit(games, processed_game)

    print("\n"*4)

    user_content_time = input("Введите продолжительность контента: ")
    if user_content_time == "": user_content_time = 0
    else: user_content_time = int(user_content_time)
    processed_game.content_time += user_content_time

    add_titles(titles, processed_game, count_videos)
    add_empty_message(empty_messages, processed_game, count_videos, message_id)
    telegram_utils.edit_caption(f"{processed_game.full_name}: № {processed_game.count_episode + 1}{f" - {processed_game.count_episode + count_videos}" if count_videos > 1 else ""}", message_id)

    stat.process_game_id = -1
    stat.process_game_message_id = -1

    processed_game.count_episode += count_videos

    move_videos(processed_game.video_dir)

def equalize_time_limit(games: list[Game], processed_game: Game):
    if processed_game.id != 2:
        processed_game.time_limit -= processed_game.user_time - 120

        difference = 120 - max(games[:2], key=lambda game: game.time_limit).time_limit

        for game in games[:2]:
            game.time_limit += difference
    
