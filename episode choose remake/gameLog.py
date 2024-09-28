print("Загрузка модуля timeFormat для gameLog...")
from timeFormat import date_position, today, end_of_month
print("Загрузка модуля pydata для gameLog...")
from pydata import *
import statisticsLog

default = [[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []]]

def game_log(name):
    week, day = date_position(today())

    log = pydata_load("game_log")

    if today() > log["next_reset"]:
        statisticsLog.save()
        log["game_log"]= default
        log["next_reset"] = end_of_month(today())

    log["game_log"][week][day].append(name)
    pydata_save(log, "game_log")

if __name__ == "__main__":
    game_log("Mafia II: Definitive Edition")