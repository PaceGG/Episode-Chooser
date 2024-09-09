import json
import os
import PATHS
from moviepy.video.io.VideoFileClip import VideoFileClip

os.chdir(PATHS.repository)

def get_total_duration_of_file(directory):
    """returns a duration of videos in directory in seconds and number of videos"""
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

video_paths = [os.path.join(PATHS.video, game["name"].replace(":", "")) for game in data] + ["D:/Program Files/Shadow Play/SnowRunner"]

dirs = {}

total_duration, number_of_videos = get_total_duration_of_file(video_paths[0])
dirs[data[0]["name"]] = {"total_duration": total_duration, "number_of_videos": number_of_videos}

total_duration, number_of_videos = get_total_duration_of_file(video_paths[1])
dirs[data[1]["name"]] = {"total_duration": total_duration, "number_of_videos": number_of_videos}

total_duration, number_of_videos = get_total_duration_of_file(video_paths[2])
dirs["SnowRunner"] = {"total_duration": total_duration, "number_of_videos": number_of_videos}

def get_total_duration(game_name):
    try: return dirs[game_name]["total_duration"]
    except: return None

def get_number_of_videos(game_name):
    try: return dirs[game_name]["number_of_videos"]
    except: return None
