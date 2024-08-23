import os
from os.path import getctime

def create_game_structure(game_name):
    game_path = os.path.join("D:/Program Files/Shadow Play", game_name)
    if os.path.exists(game_path):
        return int(getctime(game_path))
    os.makedirs(game_path, exist_ok=True)
    previews_path = os.path.join(game_path, "previews")
    os.makedirs(previews_path, exist_ok=True)
    print("Директории созданы")
    return int(getctime(game_path))

def icon_rename(game_name):
    directory = "D:/Program Files/HTML/Games/icons_new"
    variants = ["ng", "new_game", "new game"]
    
    for variant in variants:
        full_path = os.path.join(directory, f"{variant}.png")
        if os.path.exists(full_path):
            new_full_path = os.path.join(directory, f"{game_name}.png")
            os.rename(full_path, new_full_path)
            print(f"Файл '{full_path}' переименован в '{new_full_path}'")
            return
    print("Иконка не найдена")

if __name__ == "__main__":
    game_name = "test"
    # icon_rename(game_name)
    create_game_structure(game_name)