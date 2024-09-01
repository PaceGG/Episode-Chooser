from jsonLoader import *
path = "episode choice remake/game_log.json"

print("Загрузка модуля timeFormat для gameLog...")
from timeFormat import date_position, today, end_of_month

default = [[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []]]

def game_log(name):
    week, day = date_position(today())

    log = json_load(path)

    if today() > log["next_reset"]:
        log["game_log"]= default
        log["next_reset"] = end_of_month(today())
        # calc_statistics(log["game_log"])

    log["game_log"][week][day].append(name)
    json_save(path, log)

if __name__ == "__main__":
    game_log("Mafia II: Definitive Edition")