import os

def create_game_structure(game_name, base_directory):
    game_path = os.path.join(base_directory, game_name)
    os.makedirs(game_path, exist_ok=True)
    previews_path = os.path.join(game_path, "previews")
    os.makedirs(previews_path, exist_ok=True)
    episodes_log_path = os.path.join(previews_path, "episodes log.txt")
    with open(episodes_log_path, 'w'):
        pass

    

# Название игры
game_name = "Resident Evil 7"



base_directory = "D:/Program Files/Shadow Play"
create_game_structure(game_name, base_directory)
print("Директории созданы")