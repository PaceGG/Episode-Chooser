import json
import os

def create_game_time_file(game_time_file):
    with open (game_time_file, 'w') as f: json.dump({"game_time": []}, f)

def load_game_time(video_folder):
    game_time_file = os.path.join(video_folder, "game_time.json")
    if not os.path.exists(game_time_file): create_game_time_file(game_time_file)
    with open (game_time_file, 'r') as f:
        game_time = json.load(f)["game_time"]

    return game_time

def reset_game_time(video_folder):
    game_time_file = os.path.join(video_folder, "game_time.json")
    with open (game_time_file, 'w') as f:
        json.dump({"game_time": []}, f)

def strf(n):
    if n < 0: return str(n)
    else: return "+" + str(n)

def calc_next_game_time(game_time):
    extra_time = (game_time - 120)//5
    if extra_time > 0: is_negative = 1
    else: is_negative = -1

    base = abs(extra_time) // 3
    remainder = abs(extra_time) % 3

    output = [base] * 3

    for i in range(remainder):
        output[i] += 1

    return [x*5*-1*is_negative for x in output if x != 0]

def calc_game_time(video_folder):
    game_time = load_game_time(video_folder)

    reset_game_time(video_folder)

    time_list = calc_next_game_time(120 - 40 * len(game_time) + sum(game_time))

    create_game_time_files(video_folder, time_list)

    return equalize_game_time(video_folder)

def create_game_time_files(video_folder, game_time_list):
    for time in game_time_list:
        time = strf(time) + " "
        game_time_file = os.path.join(video_folder, f"{time}")
        while os.path.exists(game_time_file):
            time += " "
            game_time_file = os.path.join(video_folder, f"{time}")

        with open (game_time_file, 'w') as f:
            pass

def delete_game_time_files(video_folder):
    files_to_delete = [f for f in os.listdir(video_folder) if f.endswith(' ')]

    for f in files_to_delete:
        file_path = os.path.join(video_folder, f)
        os.remove(file_path)

def equalize_game_time(video_folder):
    times = [int(f.rstrip(' ')) for f in os.listdir(video_folder) if f.endswith(' ')]
    delete_game_time_files(video_folder)
    create_game_time_files(video_folder, calc_next_game_time(120 - sum(times)))
    return [int(f.rstrip(' ')) for f in os.listdir(video_folder) if f.endswith(' ')]


if __name__ == "__main__":
    print(calc_game_time("D:/Program Files/Shadow Play/Fallout New Vegas"))

    pass
