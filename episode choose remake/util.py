import win32api
import win32gui
import paths
from pathlib import Path
from directory_statistics import get_disk_video

def set_eng_layout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return(result)

def move_videos(target_dir: Path, games):
    obs_dir = paths.video_dir / "OBS"
    start_index = get_disk_video(games) + 1

    for file in obs_dir.iterdir():
        if file.is_file():
            if file.suffix == ".mp4":
                new_name = f"{start_index}.mp4"
                start_index += 1
            else:
                new_name = file.name

            target_path = target_dir / new_name
            try:
                file.rename(target_path)
            except Exception as e:
                print(f"Ошибка перемещения {file}: {e}")


def create_game_folder(video_dir: Path):
    video_dir.mkdir()
    previews_dir = Path.joinpath(video_dir, "previews")
    previews_dir.mkdir()

def header_rename(game_name: str):
    headers_dir = Path.joinpath(paths.video_dir, "headers")
    header_default_path = Path.joinpath(headers_dir, "header.png") 
    header_path = Path.joinpath(headers_dir, game_name + ".png")
    try:
        header_default_path.rename(header_path)
    except:
        print("Ошибка: header отсутствует")
        while True: pass

def intc(s):
    n = ""
    for c in s:
        if c.isdigit():
            n += c

    return n

def sumtime(time: str):
    if time.count(":") == 1: time += ":00"
    time_split = time.split(":")
    return int(time_split[-2]) + int(time_split[-3]) * 60