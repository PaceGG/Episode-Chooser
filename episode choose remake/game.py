print("Загрузка модуля game")
from genericpath import getctime
from os import error
import paths
import json
from pathlib import Path
from time_format import time_format, today
from data import Data
from roulette import spin_roulette
from util import *
from youtube_utils import add_titles, add_empty_message
from directory_statistics import *
from pyperclip import paste
import telegram_utils

def get_short_name(name):
    local = {
        "Return to Castle Wolfenstein": "Wolfenstein",
        "Far Cry Primal": "Far Cry",
        "SnowRunner [ng+]": "SR",
        "Far Cry New Dawn": "Far Cry",
        "Battlefield Hardline": "Battlefield",
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
        print(f"Инициализация {name}")
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

        # self.game_path = paths.game_paths[self.id]
        if self.id != 2:
            self.game_path = find_best_match(self.name, paths.games_dir)
            if self.game_path == None:
                raise Exception(f"Ошибка инициализации {name}: Не удалось найти путь к ярлыку игры.")
        else:
            self.game_path = Path('C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs').resolve()
        self.video_dir = Path.joinpath(paths.video_dir, self.safe_name)
        if not self.video_dir.exists(): create_game_folder(self.video_dir)

        stat = Data("stat")
        with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
            if (self.name not in stat.games_list and self.id != 2):
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

        if self.count_episode == self.count_session == 0: self.is_game_new = True

        self.chance = 1
        self.is_selected = False

        self.header = Path.joinpath(paths.video_dir, "headers", self.safe_name + ".png")
        if not self.header.exists(): header_rename(self.safe_name)

    def content_time_format(self):
        content_time_debt = -self.content_time
        return f"{"+" if content_time_debt > 0 else ""}{content_time_debt}"

    def __repr__(self):
        return f"class {self.__class__.__name__}(\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())})"
    
    def as_dict(self):
        return {
            "name": self.name,
            "count_session": self.count_session,
            "count_episode": self.count_episode,
            "time_limit": self.time_limit,
            "content_time": self.content_time,
            "user_time": self.user_time
        }
    
    
def chance_calculate(games: list[Game]):
    games[0].chance = 1
    games[1].chance = 1
    games[2].chance = 0
    min(games[:2], key=lambda game: game.count_session).chance += abs(games[0].count_session - games[1].count_session)

def new_game(games: list[Game], stat: Data):
    for game in games[:2]:
        print(f"{game.name}: {game.is_game_new}")
        if game.is_game_new and stat.process_game_id == -1 and games[game.id].video_dir.stat().st_birthtime > games[not(game.id)].video_dir.stat().st_birthtime:
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

def select_game(games: list[Game], stat: Data, skip_roulette = False, make_selection = True):
    # force new game (not in game list)
    selected_game = next((game for game in games[:2] if game.is_selected), None)
    if selected_game is not None:
        return selected_game

    # force new game (episodes == 0)
    # for game in games[:2]:
    #     if game.count_episode == 0:
    #         game.is_selected = make_selection
    #         return game

    # force new game (sessions == 0 and later game)
    if games[0].count_session == games[1].count_session == 0:
        if games[0].video_dir.stat().st_birthtime < games[1].video_dir.stat().st_birthtime:
            games[1].is_selected = make_selection
            return games[1]
        else:
            games[0].is_selected = make_selection
            return games[0]
        
    # force sr
    try:
        if stat.count_sr_session <= 0 and stat.count_sr_date <= today():
            games[2].is_selected = make_selection
            return games[2]
    except:
        pass
    
    # force unpopular game (games_log)
    if len(set(stat.games_log)) == 1:
        unpopular_game = next((game for game in games[:2] if game.name not in stat.games_log), None)
        if unpopular_game is not None:
            unpopular_game.is_selected = make_selection
            return unpopular_game

    # no force
    if make_selection:
        selected_game = spin_roulette(games, skip=skip_roulette)
        selected_game.is_selected = make_selection
        return selected_game
    else:
        return False

def run_game(games: list[Game], stat: Data):
    set_eng_layout()
    selected_game = get_selected_game(games)

    input(f"Нажмите Enter, чтобы запустить {selected_game.full_name}...")

    caption = f"{selected_game.full_name} № {selected_game.count_episode + 1}... {time_format(selected_game.time_limit)} [{selected_game.content_time_format()}]"
    print(f"{selected_game.full_name}{f" {time_format(selected_game.time_limit)}" if selected_game.time_limit != 120 else ''}")
    stat.process_game_message_id = telegram_utils.send_image(selected_game.header, caption)

    
    if selected_game.id != 2:
        stat.count_sr_session -= 1
    else:
        stat.count_sr_session += 5
        stat.count_sr_date = today() + 7*24*60*60

    selected_game.count_session += 1
    chance_calculate(games)

    stat.process_game_id = selected_game.id

    return selected_game.game_path


def unfinished_process(games: list[Game], stat: Data, duration: int):
    unfinished_game = games[stat.process_game_id]

    # склонение существительного
    time_left = unfinished_game.time_limit - duration
    if time_left % 10 == 1 and time_left % 100 != 11: form = "минута"
    elif time_left % 10 in {2, 3, 4} and not (time_left % 100 in {12, 13, 14}): form = "минуты"
    else: form = "минут"

    caption = f"{unfinished_game.full_name} № {unfinished_game.count_episode + 1}... {time_format(time_left)} [{unfinished_game.content_time_format()}]"
    telegram_utils.edit_caption(caption, stat.process_game_message_id)

    print(f"Сессия {unfinished_game.name} ещё не завершена, осталось {time_left} {form}")
    print(f"Запустить {unfinished_game.name}? Введите \"-\" для обозначения финальной сессии")
    confirm = input()
    if confirm == "-": return None, True
    return unfinished_game.game_path, False

def finished_process(games: list[Game], stat: Data, empty_messages, titles, is_last_session, duration): 
    process_game_id = stat.process_game_id
    message_id = stat.process_game_message_id
    processed_game = games[process_game_id]

    if is_last_session: duration = 120
    count_videos = get_count_videos()

    if not is_last_session:
        print(f"В {processed_game.name} есть видео продолжительностью {duration} минут. Добавить их к сумме? Введите \"-\" для обозначения финальной сессии")
        user_time = input(f"Введите время для {processed_game.name}: ")
    else:
        user_time = "-"

    if user_time == "": user_time = duration
    elif user_time == "-":
        user_time = games[process_game_id].time_limit
        is_last_session = True
    elif ":" in user_time: user_time = sumtime(user_time)
    else: user_time = int(user_time)
    processed_game.user_time = user_time
    equalize_time_limit(games, stat)

    if processed_game.id != 2:
        stat.add_game_log(processed_game.name)

    print("\n"*4)


    if not is_last_session:
        try:
            bufer_user_content_time = sumtime(paste().split("\n")[-2].split()[1]) - 40 * get_count_videos()
            print(f"В буфере обмена есть время контента: {bufer_user_content_time}")
        except:
            bufer_user_content_time = 0
        user_content_time = input("Введите \"-\" для обозначения финальной сессии. Введите продолжительность контента: ")
    else:
        user_content_time = 0

    if user_content_time == "": user_content_time = bufer_user_content_time
    elif ":" in str(user_content_time):
        user_content_time = sumtime(user_content_time) - 40 * get_count_videos()
    elif " " in str(user_content_time):
        user_content_time = sum([int(i) for i in user_content_time.split(" ") if i != ""]) - 40 * get_count_videos()
    elif user_content_time == "-":
        user_content_time = 0
        processed_game.content_time = 0
        is_last_session = True
    else:
        user_content_time = int(user_content_time)
    processed_game.content_time += user_content_time

    add_titles(titles, processed_game, count_videos, is_last_session)
    add_empty_message(empty_messages, processed_game, count_videos, message_id)
    telegram_utils.edit_caption(f"{processed_game.full_name}: № {processed_game.count_episode + 1}{f"-{processed_game.count_episode + count_videos}" if count_videos > 1 else ""}", message_id)

    telegram_utils.delete_message(stat.time_info_message_id)
    stat.time_info_message_id = -1
    
    stat.process_game_id = -1
    stat.process_game_message_id = -1

    processed_game.count_episode += count_videos

    move_videos(processed_game.video_dir, games)

def equalize_time_limit(games: list[Game], stat: Data):
    processed_game = games[stat.process_game_id]

    processed_game.time_limit -= processed_game.user_time - 120

    if processed_game.id != 2:
        difference = 120 - max(games[:2], key=lambda game: game.time_limit).time_limit

        for game in games[:2]:
            game.time_limit += difference
            game.user_time = 0

            if game.time_limit <= 0:
                game.time_limit += 120
                game.count_session += 1
                stat.count_sr_session -= 1
                stat.add_game_log(game.name)
    else:
        processed_game.user_time = 0
        if processed_game.time_limit <= 0:
            processed_game.time_limit += 120
            processed_game.count_session += 1
            stat.count_sr_session += 5
            stat.count_sr_date = today() + 7*24*60*60
