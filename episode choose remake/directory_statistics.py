print("Загрузка модуля directory_statistics")
import paths
from pathlib import Path
import json
from util import video_formats

def get_duration():
    from moviepy.video.io.VideoFileClip import VideoFileClip

    with open(Path.joinpath(paths.root_dir, 'data.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)
    cache = data["cache"]["durations"]

    updated_cache = {}

    total = 0

    for file_path in Path.joinpath(paths.video_dir, "OBS").iterdir():
        if file_path.suffix in video_formats:
            ctime = str(file_path.stat().st_birthtime)
            if ctime in list(cache.keys()):
                video_duration = cache[ctime]
            else:
                try:
                    with VideoFileClip(str(file_path)) as video: video_duration = video.duration
                except:
                    continue
            updated_cache[ctime] = video_duration
            total += video_duration

    data["cache"]["durations"] = updated_cache
    with open(Path.joinpath(paths.root_dir, 'data.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return int(total//60)
                
def get_count_videos(dir=Path.joinpath(paths.video_dir, "OBS")):
    c = 0
    for file_path in dir.iterdir():
        if file_path.suffix in video_formats:
            c += 1

    return c

def get_disk_video(games):
    # c = get_count_videos()
    c = 0
    for game in games:
        c += get_count_videos(game.video_dir)

    return c
