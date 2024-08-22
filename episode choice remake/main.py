import os
os.chdir("D:\\Program Files\\HTML\\Games")
import json
from time import time
from random import randint
from YT import add_empty_message, edit_empty_messages
from episodesManipulate import reset_console_flag


# modules
from setEngLayout import set_eng_layout
from telegramFunctions import edit_telegram_message, send_image
from classGame import Game

with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)["showcase"]

with open("episode choice remake/pydb.json", encoding="utf-8") as f:
    pydata = json.load(f)

start_time = time()
print("start:", time()-start_time)

# game init
game = [Game(name=item["name"]) for item in data]
game.append(Game(name="SnowRunner", short_name="SR"))

print("games done", time()-start_time)
# game paths
game[0].path = r"C:\Users\yura3\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\New Vegas EE.lnk"
game[1].path = r"C:\Users\yura3\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\deadspace3.lnk"
game[2].path = 'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'

# Chance Count
earlier, later = sorted(game[:2], key=lambda g: g.date)[0].name, sorted(game[:2], key=lambda g: g.date)[1].name

if game[0].last_session == 0 or game[1].last_session == 0:
    if game[0].last_session == 0: pydata["start_from"] = game[1].last_session
    if game[1].last_session == 0: pydata["start_from"] = game[0].last_session

    with open("episode choice remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f, indent=4)

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

def get_unpopular_game(games_log = pydata["games_log"]):
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
    name = G.name

    pydata["episodes_log"][name][0] += 1

    for g in game:
        if g.name == name:
            g.last_session += 1
            count_chance()

    if name == "SnowRunner":
        pydata["episodes_log"][name][1] += 1

    else: pydata["episodes_log"][name][1] += (not zero_flag) * 3

    with open("episode choice remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f, indent=4)

def sr_db_edit():
    if pydata["games_for_sr_counter"] == 0:
        sr_db_clear()
        return
    pydata["games_for_sr_counter"] -= 1

    with open("episode choice remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f, indent=4)
    

def sr_db_clear():
    pydata["games_for_sr_counter"] = 5

    with open("episode choice remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f, indent=4)

def edit_tg_info_message():
    # Для новой игры
    if game[0].last_session == game[1].last_session == 0:
        sr_counter_message = f"• SR: {pydata['games_for_sr_counter']}"
        chance_info_message = f"Forece: {later}"

        edit_telegram_message(f"{sr_counter_message}\n{chance_info_message}")
        return
    
    # Для старой игры
    if get_unpopular_game() is not None: force_info_message = f"• Force: {get_unpopular_game()}"
    else: force_info_message = ""

    count_chance()
    if game[0].chance == game[1].chance == 1: chance_info_message = "• Шансы равны"
    elif game[0].chance > 1: chance_info_message = f"• {game[0].short_name}: {game[0].chance}"
    elif game[1].chance > 1: chance_info_message = f"• {game[1].short_name}: {game[1].chance}"

    if pydata["games_for_sr_counter"] != 0: sr_counter_message = f"• SR: {pydata['games_for_sr_counter']}"
    else: sr_counter_message = f"• Сегодня SnowRunner!!! • {game[2].short_name}: {game[2].time_format}" if game[2].time != 120 else "• Сегодня SnowRunner!!!"

    time_format_message = ""
    for g in game:
        if g.time != 120: time_format_message += f"• {g.short_name}: {g.time_format}\n"

    edit_telegram_message(f"{sr_counter_message}\n{force_info_message}\n{chance_info_message}\n\n{time_format_message}")


def add_game_log(game_name):
    pydata["games_log"] = pydata["games_log"][1:] + [game_name]



    with open("episode choice remake/pydb.json", "w", encoding="utf-8") as f:
        json.dump(pydata, f, indent=4)

def snowrunner_updater():
    os.utime("D:/Program Files/Shadow Play/SnowRunner", (time(), time()))


def run_game(game_to_run):
    set_eng_layout()
    if game_to_run.time <= 0:
        pydata["episodes_time"][game_to_run.name]["time"] += 120
        add_episode(game_to_run, True)
    else:
        print(f"{game_to_run.name}{f" {game_to_run.long_time_format}" if game_to_run.time != 120 else ""}")
        game_message_id = send_image(game_to_run.icon, game_to_run.caption)
        add_empty_message(game_to_run.name, [game_to_run.last_episode+1, game_to_run.last_episode+3], game_message_id)
        add_episode(game_to_run)
    add_game_log(game_to_run.name)
    sr_db_edit()
    edit_tg_info_message()
    reset_console_flag(game_to_run.name)
    os.startfile(game_to_run.path)
    

def get_game(name):
    for g in game:
        if g.name == name:
            return g

def run_random_game():
    print("\n"*10)
    confirm = input()

    if game[0].last_session == 0 and game[1].last_session == 0:
        sr_db_clear()
        if earlier == game[0].name: run_game(game[1])
        if earlier == game[1].name: run_game(game[0])
    elif pydata["games_for_sr_counter"] != 0:
        run_game(get_game(choice))
    else:
        run_game(game[2])
        snowrunner_updater()

def print_info():
    if pydata["games_for_sr_counter"] == 1:
        ep_prefix = 'я'
    elif 1 < pydata["games_for_sr_counter"] < 5:
        ep_prefix = 'и'
    else:
        ep_prefix = 'й'

    if pydata["games_for_sr_counter"] > 0:
        print(f"До SnowRunner'a ещё {pydata['games_for_sr_counter']} сери{ep_prefix}")
        print()
    else:
        print(f"Сегодня SnowRunner: {game[2].long_time_format}")
        print()

    if chose_method == "force":
        print(f"Force: {choice}")
    
    for i in range(2):
        g = game[i]
        if g.chance != 1: print(f"{g.name}: {g.chance}")
    
    if game[0].chance == game[1].chance == 1: print("Шансы равны")

    print()

    for i in range(2):
        g = game[i]
        if g.time != 120: print(f"{g.name}: {g.long_time_format}")

    edit_tg_info_message()
    

if __name__ == "__main__":
    edit_empty_messages()
    print_info()
    # run_random_game()
    pass

