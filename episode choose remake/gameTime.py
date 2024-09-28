import json
import os

from pydata import *

def load_game_time(game_name):
    game_time_data = pydata_load("game_time")

    try:
        return game_time_data[game_name]
    except KeyError:
        game_time_data[game_name] = { "game_time": [], "time_to_play": [] }
        pydata_save(game_time_data, "game_time")
        return game_time_data[game_name]

def strf(n):
    if n < 0: return str(n)
    else: return "+" + str(n)

def calc_next_game_time(game_time):
    extra_time = int((game_time - 120)/5)
    if extra_time > 0: is_negative = 1
    else: is_negative = -1

    base = abs(extra_time) // 3
    remainder = abs(extra_time) % 3

    output = [base] * 3

    for i in range(remainder):
        output[i] += 1

    return [x*5*-1*is_negative for x in output if x != 0]

def calc_game_time(game_name):
    game_time_data = load_game_time(game_name)
    game_time = game_time_data["game_time"]
    time_to_play = game_time_data["time_to_play"]

    time_to_play.extend(calc_next_game_time(120 - 40 * len(game_time) + sum(game_time)))
    time_to_play = equalize_game_time(time_to_play)

    game_time_data["game_time"] = []
    game_time_data["time_to_play"] = time_to_play

    data = pydata_load("game_time")
    data[game_name] = game_time_data
    pydata_save(data, "game_time")

    return str([strf(x) for x in time_to_play]).replace(",", ";").replace("'", "")

def save_time_to_play(game_name, time_to_play):
    game_time_data = pydata_load("game_time")
    game_time_data[game_name]["time_to_play"] = time_to_play
    pydata_save(game_time_data, "game_time")

def equalize_game_time(time_to_play):
    return calc_next_game_time(sum(calc_next_game_time(sum(time_to_play))))


if __name__ == "__main__":
    print(calc_game_time("Return to Castle Wolfenstein"))

    pass
