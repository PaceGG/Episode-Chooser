import json
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
root_dir = Path(__file__).resolve().parent
site_db_path = Path.joinpath(project_dir, "react-remake\\db.json")

import local_data
games_dir = local_data.games_dir
video_dir = local_data.video_dir

extra_names = [
    "", # First game
    "", # Second game
    "Мичиган", # Extra/third game
]

with open(site_db_path) as file:
    showcase: list[dict] = json.load(file)["showcase"]

game_names: list[str] = [game["name"] for game in showcase]
game_names.append("SnowRunner [ng+]")

game_colors: list[str] = [game["color"] for game in showcase]
game_colors.append("#FF0000")


game_paths = [
    Path.joinpath(games_dir, game_names[0].replace(':', ''), "game.lnk"),
    Path.joinpath(games_dir, game_names[1].replace(':', ''), "game.lnk"),
    Path('C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs').resolve()
]

extra_names = [
    "", # First game
    "", # Second game
    "Мичиган", # Extra/third game
]

if __name__ == "__main__":
    print(f"root_dir: {root_dir}")
    print(f"site_db_path: {site_db_path}")
    print(f"games_dir: {games_dir}")
    print(f"video_dir: {video_dir}")
    print(f"game_names: {game_names}")
    print(f"game_colors: {game_colors}")
    print(f"game_paths: {game_paths}")
    print(f"extra_names: {extra_names}")