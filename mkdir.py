import os

def create_game_structure(game_name, base_directory):
    game_path = os.path.join(base_directory, game_name)
    os.makedirs(game_path, exist_ok=True)
    previews_path = os.path.join(game_path, "previews")
    os.makedirs(previews_path, exist_ok=True)
    episodes_log_path = os.path.join(previews_path, "episodes log.txt")
    with open(episodes_log_path, 'w'):
        pass
    print("Директории созданы")

def icon_rename(game_name):
    directory = "D:\\Program Files\\HTML\\Games\\icons_new"
    variants = ["ng", "new_game", "new game"]
    
    for variant in variants:
        full_path = os.path.join(directory, f"{variant}.png")
        if os.path.exists(full_path):
            new_full_path = os.path.join(directory, f"{game_name}.png")
            os.rename(full_path, new_full_path)
            print(f"Файл '{full_path}' переименован в '{new_full_path}'")
            return
    print("Ни один из файлов не найден")
    

# Название игры
game_name = "Outer Wilds"


icon_rename(game_name)
base_directory = "D:/Program Files/Shadow Play"
create_game_structure(game_name, base_directory)