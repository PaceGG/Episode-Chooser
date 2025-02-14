import win32api
import win32gui
import paths
from pathlib import Path
from directory_statistics import get_disk_video
import difflib

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

def find_best_match(game_name: str, games_directory: Path, default_dir = Path(r"D:\Program Files\Desktop")) -> Path | None:
    folders = [folder for folder in games_directory.iterdir() if folder.is_dir()]
    folder_names = [folder.name for folder in folders]

    best_match = difflib.get_close_matches(game_name, folder_names, n=1, cutoff=0.5)


    if best_match:
        game_directory = next(folder for folder in folders if folder.name.lower() == best_match[0].lower())

        game_links = [link for link in game_directory.iterdir() if link.suffix == ".lnk"]
        best_links = difflib.get_close_matches(game_name, [link.name for link in game_links], n=1, cutoff=0.5)

        if best_links:
            best_link = next(link for link in game_links if link.name.lower() == best_links[0].lower())
        else:
            best_link = Path.joinpath(game_directory, "game.lnk")

            if not best_link.exists():
                best_links = difflib.get_close_matches(game_name, [link.name for link in default_dir.iterdir() if link.suffix == ".lnk"], n=1, cutoff=0.5)
                best_link = next(link for link in default_dir.iterdir() if link.name.lower() == best_links[0].lower())

                best_link.rename(game_directory / "game.lnk")
                best_link = Path.joinpath(game_directory, "game.lnk")

        return best_link
    else:
        return None