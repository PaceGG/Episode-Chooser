import win32api
import win32gui
import paths
from pathlib import Path
from directory_statistics import get_disk_video

def set_eng_layout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return(result)

def move_videos(files_dir: Path):
    obs_dir = Path.joinpath(paths.video_dir, "OBS")
    for i, file in enumerate(obs_dir.iterdir()):
        file.rename(Path.joinpath(files_dir, str(get_disk_video() + i + 1)))

def create_game_folder(video_dir: Path):
    video_dir.mkdir()
    previews_dir = Path.joinpath(video_dir, "previews")
    previews_dir.mkdir()

def header_rename(game_name: str):
    headers_dir = Path.joinpath(paths.video_dir, "headers")
    header_default_path = Path.joinpath(headers_dir, "header.png") 
    header_path = Path.joinpath(headers_dir, game_name + ".png")
    header_default_path.rename(header_path)

def intc(s):
    n = ""
    for c in s:
        if c.isdigit():
            n += c

    return n
