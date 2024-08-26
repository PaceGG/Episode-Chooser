import json
import os

def load_game_time(video_folder):
    game_time_file = os.path.join(video_folder, "game_time.json")
    with open (game_time_file, 'r') as f:
        game_time = json.load(f)["game_time"]

    return game_time

def reset_game_time(video_folder):
    game_time_file = os.path.join(video_folder, "game_time.json")
    with open (game_time_file, 'w') as f:
        json.dump({"game_time": []}, f)

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

    return calc_next_game_time(120 - 40 * len(game_time) + sum(game_time))




if __name__ == "__main__":
    print(calc_game_time("D:/Program Files/Shadow Play/Dead Space 3"))
