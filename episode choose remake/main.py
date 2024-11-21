from rollback import save_rollback
save_rollback()

print("Загрузка...")
import PATHS
import os
from psutil import disk_usage
os.chdir(PATHS.repository)
import json
from random import randint

# modules
print("Загрузка модуля YT...")
from YT import add_empty_message, edit_empty_messages
print()

print("Загрузка модуля episodesManipulate...")
from episodesManipulate import reset_console_flag, add_last_time, add_game_log, sr_db_update, snowrunner_updater, add_quiet_time, get_last_object
print()

print("Загрузка модуля setEngLayout...")
from setEngLayout import set_eng_layout
print()

print("Загрузка модуля telegramFunctions...")
from telegramFunctions import edit_telegram_message, send_image
print()

print("Загрузка модуля classGame...")
from classGame import Game
print()

print("Загрузка модуля pydata...")
from pydata import pydata_load, pydata_save
print()

print("Загрузка модуля timeFormat...")
from timeFormat import short_date_format, pc_date_format, today
print()

print("Загрузка модуля gameLog...")
from gameLog import game_log
print()

print("Загрузка модуля YTTitle...")
from YTTitle import add_yt_titles
print()

print("Загрузка модуля totalDuration...")
from totalDuration import get_total_duration, get_number_of_videos, get_last_local_episode
print()

print("Загрузка модуля showimg...")
from showimg import show_image
print()

# functions
# information and statistics functions
def edit_tg_info_message():
    pydata = pydata_load()

    # sr_counter_message
    if pydata["games_for_sr_counter"] > 0: sr_counter_message = f"• SR: {pydata['games_for_sr_counter']}"
    elif pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] > today(): sr_counter_message = f"SR: {short_date_format(pydata['time_for_sr_counter'])}"
    else: sr_counter_message = f"• Сегодня SnowRunner!!! • {game[2].short_name}: {game[2].time_format}" if game[2].time != 120 else "• Сегодня SnowRunner!!!"

    # force_info_message
    check_frequency()
    force_info_message = f"\n• Force: {choose.short_name}" if is_choose_forced else ""

    # chance_info_message
    count_chance()
    if game[0].chance == game[1].chance == 1: chance_info_message = "• Шансы равны"
    elif game[0].chance > 1: chance_info_message = f"• {game[0].short_name}: {game[0].chance}"
    elif game[1].chance > 1: chance_info_message = f"• {game[1].short_name}: {game[1].chance}"

    # time_info_message
    time_info_message = ""
    for g in game:
        time = g.time_format
        if g.time == 120: time = ""

        game_time = g.game_time
        if game_time == []: game_time = ""

        msg = f"• {g.short_name}: "

        if time: msg += f"{time}"
        if game_time != "[]": msg += game_time

        if msg != f"• {g.short_name}: ": time_info_message += msg + "\n"

    # time_for_sr_message
    time_for_sr_message = f"SR after {pc_date_format(pydata['time_for_sr_counter'])}\n" if pydata["time_for_sr_counter"] > today() else ""

    # next_update_message
    next_update_message = f"Next Update: {pc_date_format(pydata["last_update"] + 12*60*60)}"

    edit_telegram_message(f"{sr_counter_message}\n{force_info_message}\n{chance_info_message}\n\n{time_info_message}\n{time_for_sr_message}{next_update_message}")

def print_info():
    edit_empty_messages()
    os.system('cls')
    pydata = pydata_load()
    yt_titles = pydata_load("game_log_YTTitle")

    free_space = disk_usage(PATHS.video).free/1024/1024/1024
    print(f"Место на диске: {free_space:.2f} GB ~ {int(free_space//15)} видео")
    print(f"Видео к удалению: {max(get_last_local_episode() - len(yt_titles), 0)}")

    print()

    # snowrunner info "До SnowRunner'a ещё 3 сессии" or "SnowRunner после 05.01.2022"
    ep_prefix = 'я' if abs(pydata["games_for_sr_counter"]) == 1 else ('и' if 1 < abs(pydata["games_for_sr_counter"]) < 5 else 'й')

    if pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] <= today(): print(f"Сегодня SnowRunner: {game[2].long_time_format}")
    elif pydata["games_for_sr_counter"] > 0: print(f"До SnowRunner'a ещё {pydata['games_for_sr_counter']} сесси{ep_prefix}")
    else: print(f"SnowRunner после {pc_date_format(pydata['time_for_sr_counter'])}")

    print()

    # force info "Force: Fallout: New Vegas"
    if is_choose_forced: print(f"Force: {choose.name}")
    
    # chance info "Шансы равны" or "Fallout: 2"
    for i in range(2):
        g = game[i]
        if g.chance != 1: print(f"{g.name}: {g.chance}")
    if game[0].chance == game[1].chance == 1: print("Шансы равны")

    print()

    # time info "Fallout: New Vegas: ::((21) / (31) / 01:01 (61))::"
    for i in range(2):
        g = game[i]
        if g.time != 120: print(f"{g.name}: {g.long_time_format}")

    print()

    #game time info "Fallout: New Vegas: [-5, -5]"
    for g in game[:2]:
        game_time = g.game_time
        if game_time != "[]": print(f"{g.name}: {game_time}")

    edit_tg_info_message()


# run game functions
def add_episode(G: Game):
    global game
    pydata = pydata_load()
    name = G.name

    pydata["episodes_log"][name][0] += 1

    for g in game:
        if g.name == name:
            g.last_session += 1
            count_chance()

    if name == "SnowRunner": pydata["episodes_log"][name][1] += 1
    else: pydata["episodes_log"][name][1] += (G.time > 0) * 3

    pydata_save(pydata)

def run_game(game_to_run: Game):
    confirm = input()
    if game_to_run.time <= 0:
        add_quiet_time(game_to_run.name)
    else:
        print(f"{game_to_run.name}{f" {game_to_run.long_time_format}" if game_to_run.time != 120 else ""}")
        game_message_id = send_image(game_to_run.header, game_to_run.caption)
        add_empty_message(game_to_run.extra_name, [game_to_run.last_episode+1, game_to_run.last_episode+3], game_message_id)
    if game_to_run.name != "SnowRunner":
        add_game_log(game_to_run.name)
    add_episode(game_to_run)
    sr_db_update(game_to_run.name)
    edit_tg_info_message()
    reset_console_flag(game_to_run.name)
    game_log(game_to_run.name)
    add_last_time(game_to_run.name)
    show_image(game_to_run.header)
    os.startfile(game_to_run.path)

def uncomplited_session():
    pydata = pydata_load()
    for g in game:
        if pydata["episodes_time"][g.name]["add_by_console"] == "False": return g

    return None

def run_random_game():
    print("\n"*10)
    set_eng_layout()
    pydata = pydata_load()

    uncomplited_game = uncomplited_session()

    if uncomplited_game is None:
        if pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] <= today():
            snowrunner_updater()
            run_game(game[2])
        else:
            run_game(choose)
    else:
        total_duration = get_total_duration(uncomplited_game.name)
        number_of_videos = get_number_of_videos(uncomplited_game.name)
        completed_duration = total_duration // 60 - pydata["episodes_time"][uncomplited_game.name]["last_time"]
        duration = pydata["episodes_time"][uncomplited_game.name]["time"] - completed_duration
        
        # склонение существительного
        if duration % 10 == 1 and duration % 100 != 11: form = "минута"
        elif duration % 10 in {2, 3, 4} and not (duration % 100 in {12, 13, 14}): form = "минуты"
        else: form = "минут"

        print(f"Сессия {uncomplited_game.name} ещё не завершена, осталось {duration} {form}")
        print(f"Запустить {uncomplited_game.name}? Введите \"-\" для добавления серий к yt titles")
        confirm = input()
        if confirm == "-":
            add_yt_titles(uncomplited_game.name, number_of_videos - pydata["episodes_time"][uncomplited_game.name]["last_episodes"], is_last_session=True)

            empty_messages = pydata_load("YT")
            to_edit_index = get_last_object(uncomplited_game.name)[1]
            empty_messages[to_edit_index]["ep_range"][1] -= 3 - (number_of_videos - pydata["episodes_time"][uncomplited_game.name]["last_episodes"])
            pydata_save(empty_messages, "YT")

            data = pydata_load()
            data["episodes_time"][uncomplited_game.name]["add_by_console"] = "True"
            pydata_save(data)
        else:
            os.startfile(uncomplited_game.path)

# databases init
with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)["showcase"]
pydata = pydata_load()

# game init
game = [Game(name=item["name"]) for item in data]
game.append(Game(name="SnowRunner", short_name="SR"))

for i, g in enumerate(game):
    g.update_time()
    g.path = PATHS.game[i]
    g.extra_name = PATHS.extra_names[i]

# earlier and later definition
earlier, later = sorted(game[:2], key=lambda g: g.date)[0], sorted(game[:2], key=lambda g: g.date)[1]

# start from
if game[0].last_session == 0 or game[1].last_session == 0:
    pydata = pydata_load()
    if game[0].last_session == 0: pydata["start_from"] = game[1].last_session
    if game[1].last_session == 0: pydata["start_from"] = game[0].last_session
    if pydata["games_for_sr_counter"] <= 5: pydata["games_for_sr_counter"] = 5
    pydata_save(pydata)

start_from = pydata["start_from"]

if earlier.name == game[0].name: game[0].last_session -= start_from
if earlier.name == game[1].name: game[1].last_session -= start_from

# count chance
def count_chance():
    global start_from, game

    more_game = abs(game[0].last_session-game[1].last_session) + 1

    if game[0].last_session > game[1].last_session:
        game[0].chance = 1
        game[1].chance = more_game
    else:
        game[0].chance = more_game
        game[1].chance = 1

count_chance()

# select random game
def select_random_game():
    game_list = []
    for g in game:
        game_list.extend([g.name] * g.chance)

    choose = game_list[randint(0,len(game_list)-1)]

    choosen_game = game[0] if choose == game[0].name else game[1]

    return choosen_game

def get_unpopular_game():
    pydata = pydata_load()
    games_log = pydata["games_log"]
    if game[0].last_session == game[1].last_session == 0: return later
    if len(set(games_log)) == 1:
        if game[0].name not in games_log: return game[0]
        if game[1].name not in games_log: return game[1]
    return None

def check_frequency():
    global choose, is_choose_forced
    unpopular_game = get_unpopular_game()
    if unpopular_game is not None: choose, is_choose_forced = unpopular_game, True
    else: choose, is_choose_forced = select_random_game(), False

check_frequency()
    

if __name__ == "__main__":
    # print information/status
    print_info()

    # run random game
    run_random_game()