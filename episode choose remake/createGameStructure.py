import os
import json
from os.path import getctime

import PATHS

def create_game_structure(game_name):
    game_path = os.path.join(PATHS.video, game_name)
    if os.path.exists(game_path):
        return int(getctime(game_path))
    os.makedirs(game_path, exist_ok=True)
    previews_path = os.path.join(game_path, "previews")
    os.makedirs(previews_path, exist_ok=True)
    game_time_file = os.path.join(previews_path, "game_time.json")
    with open (game_time_file, 'w') as f: json.dump({"game_time": []}, f)
    print("Директории созданы")
    return int(getctime(game_path))

def rename(directory, game_name):
    icon_path = os.path.join(directory, f"{game_name}.png")

    if os.path.exists(icon_path):
        return icon_path

    variants = ["ng", "header", "new_game", "new game"]
    
    for variant in variants:
        full_path = os.path.join(directory, f"{variant}.png")
        if os.path.exists(full_path):
            new_full_path = os.path.join(directory, f"{game_name}.png")
            os.rename(full_path, new_full_path)
            return new_full_path

def icon_rename(game_name):
    directory = os.path.join(PATHS.repository, "gitignore", "icons")
    return rename(directory, game_name)

def header_rename(game_name):
    directory = os.path.join(PATHS.repository, "gitignore", "headers")
    return rename(directory, game_name)

if __name__ == "__main__":
    # game_name = "test"
    # icon_rename(game_name)
    # create_game_structure(game_name)

    print(__file__)
    print(os.path.dirname(os.path.dirname(__file__)))