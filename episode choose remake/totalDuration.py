import json
import os
import PATHS
from moviepy.video.io.VideoFileClip import VideoFileClip
from createGameStructure import create_game_structure
from pydata import pydata_load

os.chdir(PATHS.repository)

def get_total_duration(game_name):
    """returns a duration of videos in directory in seconds and number of videos"""
    directory = os.path.join(PATHS.video, game_name.replace(":", ""))

    if not os.path.exists(directory):
        create_game_structure(game_name)

    total_duration = 0
    number_of_files = 0

    print("Подсчет продолжительности серий...")
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            print("Обработка файла " + filename)
            number_of_files += 1
            file_path = os.path.join(directory, filename)
            try:
                with VideoFileClip(file_path) as video:
                    duration = video.duration
                    total_duration += int(duration)
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")

    return total_duration, number_of_files

with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)["showcase"]

games = [data[0]["name"], data[1]["name"], "SnowRunner"]

dirs = {}

for game_name in games:
    total_duration, number_of_videos = get_total_duration(game_name)
    dirs[game_name] = {"total_duration": total_duration, "number_of_videos": number_of_videos}

obs_duration, obs_number = get_total_duration("OBS")

def uncomplited_session():
    pydata = pydata_load()
    for g in games:
        if pydata["episodes_time"][g]["add_by_console"] == "False": return g
    return None

uncomplited_game = uncomplited_session()
if uncomplited_game is not None:
    dirs[uncomplited_game]["total_duration"] += obs_duration
    dirs[uncomplited_game]["number_of_videos"] += obs_number


def get_total_duration(game_name):
    try: return dirs[game_name]["total_duration"]
    except: return None

def get_number_of_videos(game_name):
    try: return dirs[game_name]["number_of_videos"]
    except: return None
