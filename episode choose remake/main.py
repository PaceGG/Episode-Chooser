print("Загрузка...")
import os
os.chdir("D:\\Program Files\\HTML\\Games")
import json
from time import time
from random import randint

# modules
print("Загрузка модуля YT...")
from YT import add_empty_message, edit_empty_messages
print()

print("Загрузка модуля episodesManipulate...")
from episodesManipulate import reset_console_flag, get_total_duration, add_last_time
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

with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)["showcase"]

# game init
game = [Game(name=item["name"]) for item in data]
game.append(Game(name="SnowRunner", short_name="SR"))

for g in game:
    g.update_time()

# game paths
game[0].path = r"C:\Users\yura3\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\New Vegas EE.lnk"
game[1].path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\BioShock Remastered\BioShock Remastered.lnk"
game[2].path = 'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'

# Chance Count
earlier, later = sorted(game[:2], key=lambda g: g.date)[0].name, sorted(game[:2], key=lambda g: g.date)[1].name

if game[0].last_session == 0 or game[1].last_session == 0:
    pydata = pydata_load()
    if game[0].last_session == 0: pydata["start_from"] = game[1].last_session
    if game[1].last_session == 0: pydata["start_from"] = game[0].last_session
    if pydata["games_for_sr_counter"] <= 5: pydata["games_for_sr_counter"] = 5

    pydata_save(pydata)

pydata = pydata_load()
start_from = pydata["start_from"]

if earlier == game[0].name: game[0].last_session -= start_from
if earlier == game[1].name: game[1].last_session -= start_from



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

game_list = []
def select_random_game(games):
    global game_list
    for game in games:
        game_list.extend([game.name] * game.chance)

    return game_list[randint(0,len(game_list)-1)]

def get_unpopular_game():
    pydata = pydata_load()
    games_log = pydata["games_log"]
    if len(set(games_log)) == 1:
        popular_game = games_log[0]
        if popular_game == game[0].name: unpopular_game = game[1].name
        elif popular_game == game[1].name: unpopular_game = game[0].name
        return unpopular_game
    return None

def check_frequency():
    if get_unpopular_game() is not None:
        return get_unpopular_game(), "force"
    return select_random_game(game), "random"
    
choice, chose_method = check_frequency()

def add_episode(G, zero_flag=False):
    global game
    pydata = pydata_load()
    name = G.name

    pydata["episodes_log"][name][0] += 1

    for g in game:
        if g.name == name:
            g.last_session += 1
            count_chance()

    if name == "SnowRunner":pydata["episodes_log"][name][1] += 1
    else: pydata["episodes_log"][name][1] += (not zero_flag) * 3

    pydata_save(pydata)
    

def sr_db_edit():
    pydata = pydata_load()
    if pydata["games_for_sr_counter"] <= 0:
        pydata["time_for_sr_counter"] = today() + 7*24*60*60
        pydata_save(pydata)
        sr_db_clear()
        return
    pydata["games_for_sr_counter"] -= 1
    pydata_save(pydata)

    

def sr_db_clear():
    pydata = pydata_load()
    pydata["games_for_sr_counter"] += 5
    pydata_save(pydata)

def edit_tg_info_message():
    pydata = pydata_load()

    # sr_counter_message
    if pydata["games_for_sr_counter"] > 0: sr_counter_message = f"• SR: {pydata['games_for_sr_counter']}"
    elif pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] > today(): sr_counter_message = f"SR: {short_date_format(pydata['time_for_sr_counter'])}"
    else: sr_counter_message = f"• Сегодня SnowRunner!!! • {game[2].short_name}: {game[2].time_format}" if game[2].time != 120 else "• Сегодня SnowRunner!!!"

    # force_info_message
    unpopular_game = get_unpopular_game()
    if unpopular_game is not None or game[0].last_session == game[1].last_session == 0: force_info_message = f"• Force: {unpopular_game}"
    else: force_info_message = ""

    # chance_info_message
    count_chance()
    if game[0].chance == game[1].chance == 1: chance_info_message = "• Шансы равны"
    elif game[0].chance > 1: chance_info_message = f"• {game[0].short_name}: {game[0].chance}"
    elif game[1].chance > 1: chance_info_message = f"• {game[1].short_name}: {game[1].chance}"

    # time_format_message aka time_info_message
    time_format_message = ""
    for g in game:
        time = g.time_format
        if g.time == 120: time = ""

        game_time = g.game_time
        if game_time == []: game_time = ""

        msg = f"• {g.short_name}: "

        if time: msg += f"{time}"
        if game_time: msg += f" {game_time}"

        if msg != f"• {g.short_name}: ": time_format_message += msg + "\n"

    # time_for_sr_message
    time_for_sr_message = f"SR after {pc_date_format(pydata['time_for_sr_counter'])}"

    # next_update_message
    next_update_message = f"Next Update: {pc_date_format(pydata["last_update"] + 12*60*60)}"

    edit_telegram_message(f"{sr_counter_message}\n{force_info_message}\n{chance_info_message}\n\n{time_format_message}\n{time_for_sr_message}\n{next_update_message}")


def add_game_log(g):
    pydata = pydata_load()
    pydata["games_log"] = pydata["games_log"][1:] + [g.name]
    pydata_save(pydata)    

def snowrunner_updater():
    os.utime("D:/Program Files/Shadow Play/SnowRunner", (time(), time()))


def run_game(game_to_run):
    pydata = pydata_load()
    if game_to_run.time <= 0:
        pydata["episodes_time"][game_to_run.name]["time"] += 120
        pydata_save(pydata)
        add_episode(game_to_run, True)
    else:
        print(f"{game_to_run.name}{f" {game_to_run.long_time_format}" if game_to_run.time != 120 else ""}")
        game_message_id = send_image(game_to_run.icon, game_to_run.caption)
        add_empty_message(game_to_run.name, [game_to_run.last_episode+1, game_to_run.last_episode+3], game_message_id)
        add_episode(game_to_run)
    if game_to_run.name != "SnowRunner":
        add_game_log(game_to_run)
    sr_db_edit()
    edit_tg_info_message()
    reset_console_flag(game_to_run.name)
    game_log(game_to_run.name)
    add_last_time(game_to_run.name)
    os.startfile(game_to_run.path)
    

def get_game(name):
    for g in game:
        if g.name == name:
            return g
        
def uncomplited_session():
    pydata = pydata_load()
    for g in game:
        if pydata["episodes_time"][g.name]["add_by_console"] == "False": return g

    return None

def run_random_game():
    print("\n"*10)
    confirm = input()
    set_eng_layout()
    pydata = pydata_load()

    if game[0].last_session == 0 and game[1].last_session == 0:
        if earlier == game[0].name: run_game(game[1])
        if earlier == game[1].name: run_game(game[0])
        return

    uncomplited_game = uncomplited_session()

    if uncomplited_game is None:
        if pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] <= today():
            run_game(game[2])
            snowrunner_updater()
        else:
            run_game(get_game(choice))
    else:
        completed_duration = get_total_duration(dir)
        duration = pydata["episodes_time"][uncomplited_game.name]["time"] - completed_duration
        
        # склонение существительного
        if duration % 10 == 1 and duration % 100 != 11: form = "минута"
        elif duration % 10 in {2, 3, 4} and not (duration % 100 in {12, 13, 14}): form = "минуты"
        else: form = "минут"

        print(f"Сессия {uncomplited_game.name} ещё не завершена, осталось {duration} {form}")
        print(f"Запустить {uncomplited_game.name}?")
        confirm = input()
        os.startfile(uncomplited_game.path)

def print_info():
    os.system('cls')
    pydata = pydata_load()
    if pydata["games_for_sr_counter"] == 1: ep_prefix = 'я'
    elif 1 < pydata["games_for_sr_counter"] < 5: ep_prefix = 'и'
    else: ep_prefix = 'й'

    # snowrunner info "До SnowRunner'a ещё 3 серии" or "SnowRunner после 05.01.2022"
    if pydata["games_for_sr_counter"] <= 0 and pydata["time_for_sr_counter"] <= today():
        print(f"Сегодня SnowRunner: {game[2].long_time_format}")
    elif pydata["games_for_sr_counter"] > 0:
        print(f"До SnowRunner'a ещё {pydata['games_for_sr_counter']} сери{ep_prefix}")
    else:
        print(f"SnowRunner после {pc_date_format(pydata['time_for_sr_counter'])}")

    print()

    # force info "Force: Fallout: New Vegas"
    if chose_method == "force":
        print(f"Force: {choice}")
    if game[0].last_session == game[1].last_session == 0:
        print(f"Force: {later}")
    
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
        if game_time: print(f"{g.name}: {game_time}")

    edit_tg_info_message()
    

if __name__ == "__main__":
    edit_empty_messages()
    print_info()
    run_random_game()
    pass
    #test commit 2