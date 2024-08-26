import json
from timeFormat import date_position, today, end_of_month

def load_log():
    with open('episode choice remake/game_log.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    
def save_log(log):
    with open('episode choice remake/game_log.json', 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=4)

default = [[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []],[[], [], [], [], [], [], []]]

def game_log(name):
    week, day = date_position(today())

    log = load_log()

    if today() > log["next_reset"]:
        log["game_log"]= default
        log["next_reset"] = end_of_month(today())
        # calc_statistics(log["next_reset"])

    log["game_log"][week][day].append(name)
    save_log(log)

    


if __name__ == "__main__":
    game_log("Mafia II: Definitive Edition")