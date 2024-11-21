import json
import os
from time import time

print("Загрузка модуля pydata для episodesManipulate...")
from pydata import *
print("Загрузка модуля YT для episodesManipulate...")
from YT import get_last_object
print("Загрузка модуля YTTitle для episodesManipulate...")
from YTTitle import add_yt_titles
print("Загрузка модуля timeFormat для episodesManipulate...")
from timeFormat import today
print("Загрузка модулей для episodesManipulate завершена")
from totalDuration import get_total_duration, get_number_of_videos
from moveContents import move_files

import PATHS

def get_old_name(new_name, data_key):
    data = pydata_load()
    with open("react-remake/db.json", encoding="utf-8") as f:
        showcase = json.load(f)["showcase"]
        actual_names = [game["name"] for game in showcase]
    old_names = [name for name in list(data[data_key].keys()) if name != "SnowRunner"]

    if old_names==actual_names or old_names == reversed(actual_names): return None

    for name in old_names:
        if name not in actual_names and new_name not in old_names:
            return name

    return None

def replace_game_data(new_name, data_key):
    old_name = get_old_name(new_name, data_key)

    if old_name is None:
        return new_name
    
    data = pydata_load()
    if data_key == "episodes_time":
        default_value = {"time": 120, "my_time": "", "last_time": 0, "last_episodes": 0, "add_by_console": "True"}
    elif data_key == "episodes_log":
        default_value = [0, 0]

    data[data_key].pop(old_name)
    data[data_key][new_name] = default_value

    pydata_save(data)
    return new_name

def add_last_time(game_name):
    data = pydata_load()
    total_duration = get_total_duration(game_name)
    number_of_files = get_number_of_videos(game_name)
    data["episodes_time"][game_name]["last_time"] = total_duration//60
    data["episodes_time"][game_name]["last_episodes"] = number_of_files
    pydata_save(data)

def count_dir_time(check_name):
    data = pydata_load()
    empty_messages = pydata_load("YT")

    game_names = [name for name in data["episodes_time"].keys()]

    for game_name in game_names:
        if game_name == check_name and data["episodes_time"][game_name]["add_by_console"] == "False":
            dir_duration = get_total_duration(game_name)
            number_of_files = get_number_of_videos(game_name)
            dir_duration//=60
            dir_duration-=data["episodes_time"][game_name]["last_time"]
            if dir_duration >= data["episodes_time"][game_name]["time"]:
                os.system("cls")
                print(f"В {game_name} есть видео продолжительностью {dir_duration} минут. Добавить их к сумме?")
                my_time = input(f"Введите время для {game_name}: ")
                if my_time == "": my_time = str(dir_duration)
                data["episodes_time"][game_name]["my_time"] = my_time
                if my_time != "": data["episodes_time"][game_name]["add_by_console"] = "True"

                data["episodes_log"][game_name][1] -= 3 - number_of_files

                to_edit_index = get_last_object(game_name)[1]
                empty_messages[to_edit_index]["ep_range"][1] -= 3 - number_of_files

                pydata_save(data)
                pydata_save(empty_messages, "YT")

                add_yt_titles(game_name)

                print("\n"*4)

                game_time_input = input("Введите продолжительность контента (game_time):")
                if game_time_input == "": game_time_input = "40 40 40"
                game_time = [int(i) for i in game_time_input.split(" ")]
                game_time_data = pydata_load("game_time")
                game_time_data[game_name]["game_time"] = game_time
                pydata_save(game_time_data, "game_time")

                move_files(os.path.join(PATHS.video, "OBS"), os.path.join(PATHS.video, game_name.replace(":", "")))
            else:
                return game_name
            
def time_sum(my_time):
    my_time = my_time.split(",")
    for i, time in enumerate(my_time):
        time = time.split(":")
        if len(time) == 2:
            time = int(time[0]) * 60 + int(time[1])
        else:
            time = int(time[0])
        my_time[i] = time
    return sum(my_time)

def get_time(name):
    count_dir_time(name)

    data = pydata_load()
    try:
        time_data = data["episodes_time"][replace_game_data(name, "episodes_time")]
    except KeyError:
        time_data = {"time": 120, "my_time": "", "last_time": 0, "last_episodes": 0, "add_by_console": "True"}

    time = time_data["time"]
    my_time = time_data["my_time"]

    if my_time == "": return time

    my_time = time_sum(my_time)

    extra_time = my_time - time
    time = 120 - extra_time

    time_data["time"] = time
    time_data["my_time"] = ""

    data["episodes_time"][name] = time_data
    pydata_save(data)

    if name != "SnowRunner": equalize_time()
    elif name == "SnowRunner": equalize_time_sr()

    data = pydata_load()
    return data["episodes_time"][name]["time"]

def equalize_time():
    data = pydata_load()
    times_to_equalize = {name: time["time"] for name, time in data["episodes_time"].items() if name != "SnowRunner"}
    times_list = list(times_to_equalize.values())
    e0 = times_list[0]
    e1 = times_list[1]
    p1 = 120 - e0
    p2 = 120 - e1
    pmin = min(p1, p2)
    e0 += pmin
    e1 += pmin
    equalized_times = {name: (e0 if i == 0 else e1) for i, name in enumerate(times_to_equalize.keys())}
    for name, new_time in equalized_times.items():
        if name in data["episodes_time"]:
            data["episodes_time"][name]["time"] = new_time

    pydata_save(data)

def equalize_time_sr():
    data = pydata_load()

    sr_time = data["episodes_time"]["SnowRunner"]["time"]

    if sr_time <= 0:
        data["episodes_time"]["SnowRunner"]["time"] = 120 + sr_time
        data["games_for_sr_counter"] += 5

    pydata_save(data)

#not optimized!
def get_episodes(name):
    data = pydata_load()
    try:
        return data["episodes_log"][replace_game_data(name, "episodes_log")][:2]
    except KeyError:
        return [0, 0]

def reset_console_flag(name):
    data = pydata_load()
    data["episodes_time"][name]["add_by_console"] = "False"
    pydata_save(data)

def add_game_log(game_name):
    pydata = pydata_load()
    pydata["games_log"] = pydata["games_log"][1:] + [game_name]
    pydata_save(pydata)

def add_quiet_time(game_name):
    pydata = pydata_load()
    pydata["episodes_time"][game_name]["time"] += 120
    pydata_save(pydata)

# SnowRunner Manipulate
def sr_db_update(game_name):
    pydata = pydata_load()
    if game_name == "SnowRunner":
        pydata["games_for_sr_counter"] += 5
        pydata["time_for_sr_counter"] = today() + 7*24*60*60
    else:
        pydata["games_for_sr_counter"] -= 1

    pydata_save(pydata)

def snowrunner_updater():
    os.utime(os.path.join(PATHS.video, "SnowRunner"), (time(), time()))

if __name__ == "__main__":

    # start_time = time()
    # print("start time: ", time() - start_time)
    # print(get_episodes("Fallout: New Vegas"))
    # print("end time: ", time() - start_time)
    # print(get_time("SnowRunner"))

    # print(get_old_name("episodes_log"))

    # replace_game_data("VLADiK BRUTAL", "episodes_log")

    # print(get_episodes("Fallout: New Vegas"))
    # print(get_time("Fallout: New Vegas"))
    # print()
    # print(get_episodes("VLADiK BRUTAL"))
    # print(get_time("VLADiK BRUTAL"))

    print(get_total_duration("Fallout: New Vegas"))
    print(get_total_duration("BioShock Remastered"))

    pass