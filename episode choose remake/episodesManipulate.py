import json
import os

print("Загрузка класса VideoFileClip для epiosdesManipulate...")
# from moviepy.video.io.VideoFileClip import get_total_duration
from moviepy.video.io.VideoFileClip import VideoFileClip
print("Загрузка модуля pydata для episodesManipulate...")
from pydata import *
print("Загрузка модуля YT для episodesManipulate...")
from YT import get_last_object
print("Загрузка модуля YTTitle для episodesManipulate...")
from YTTitle import add_yt_titles
print("Загрузка модулей для episodesManipulate завершена")

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
        default_value = {"time": 120, "my_time": "", "add_by_console": "False"}
    elif data_key == "episodes_log":
        default_value = [0, 0]

    data[data_key].pop(old_name)
    data[data_key][new_name] = default_value

    pydata_save(data)
    return new_name

def add_last_time(game_name):
    data = pydata_load()
    dir = os.path.join("D:/Program Files/Shadow Play", game_name.replace(":", ""))
    data["episodes_time"][game_name]["last_time"] = get_total_duration(dir)[0]//60
    pydata_save(data)

def count_dir_time(check_name):
    data = pydata_load()
    empty_messages = pydata_load("YT")

    game_names = [name for name in data["episodes_time"].keys()]

    for game_name in game_names:
        dir = os.path.join("D:/Program Files/Shadow Play", game_name.replace(":", ""))
        if os.path.exists(dir) and game_name == check_name and data["episodes_time"][game_name]["add_by_console"] == "False":
            dir_duration, number_of_files = get_total_duration(dir)
            dir_duration//=60
            dir_duration-=data["episodes_time"][game_name]["last_time"]
            if dir_duration > data["episodes_time"][game_name]["time"]:
                os.system("cls")
                print(f"В {game_name} есть видео продолжительностью {dir_duration} минут. Добавить их к сумме?")
                my_time = input(f"Введите время для {game_name}: ")
                data["episodes_time"][game_name]["my_time"] = my_time
                if my_time != "": data["episodes_time"][game_name]["add_by_console"] = "True"

                # test is need to make check flag
                if 3 - number_of_files > 0:
                    data["episodes_log"][game_name][1] -= 3 - number_of_files

                    to_edit_index = get_last_object(game_name)[1]
                    empty_messages[to_edit_index]["ep_range"][1] -= 3 - number_of_files

                pydata_save(data)
                pydata_save(empty_messages, "YT")

                add_yt_titles(game_name)
            else:
                return game_name
            
def get_total_duration(directory):
    total_duration = 0
    number_of_files = 0

    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            number_of_files += 1
            file_path = os.path.join(directory, filename)
            try:
                with VideoFileClip(file_path) as video:
                    duration = video.duration
                    total_duration += int(duration)
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")

    return total_duration, number_of_files
            

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
        time_data = {"time": 120, "my_time": "", "add_by_console": "False"}

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

    print(get_total_duration("D:/Program Files/Shadow Play/Fallout New Vegas"))
    print(get_total_duration("D:/Program Files/Shadow Play/BioShock Remastered"))

    pass