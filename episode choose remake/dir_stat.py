import os
import PATH
from pathlib import Path
from Data import Data
from moviepy.video.io.VideoFileClip import VideoFileClip
import json

os.chdir(PATH.root_dir)

def get_duration():
    with open("data.json", 'r', encoding='utf-8') as file:
        data = json.load(file)
    cache = data["cache"]["durations"]

    updated_cache = {}

    for file_path in Path.joinpath(PATH.video_dir, "OBS").iterdir():
        if file_path.suffix == ".mp4":
            ctime = str(file_path.stat().st_birthtime)
            if ctime in list(cache.keys()):
                video_duration = cache[ctime]
            else:
                with VideoFileClip(str(file_path)) as video: video_duration = video.duration
            updated_cache[ctime] = video_duration

    data["cache"]["durations"] = updated_cache
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return int(sum(updated_cache.values())//60)
                
def get_count_videos(dir=Path.joinpath(PATH.video_dir, "OBS")):
    c = 0
    for file_path in dir.iterdir():
        if file_path.suffix == ".mp4":
            c += 1

    return c

def get_disk_video(games):
    # c = get_count_videos()
    c = 0
    for game in games:
        c += get_count_videos(game.video_dir)

    return c
