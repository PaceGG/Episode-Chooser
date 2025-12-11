import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from time_format import end_of_month, today, yy_mm_to_unix

def load_sessions(start_date=0, end_date=today()):
    with open(r"D:\Program Files\HTML\Episode-Chooser\react-remake\public\sessions.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    return {k: v for k, v in data.items() if v["datetime"] >= start_date and v["datetime"] <= end_date}

def print_sessions(sessions):
    for s in sessions:
        session = sessions[s]

        print(session)
        print()

def make_month_recap(date):
    """
    :param date: дата формата YY-MM (25-08)
    """
    # Загрузка данных
    start_date = yy_mm_to_unix(date)
    data = load_sessions(start_date=start_date, end_date=end_of_month(start_date))

    recap = {
        "total_episodes": 0,
        "total_sessions": 0,
    }

    game_data = {}

    # Количество эпизодов
    for session_id, session_data in data.items():
        game = session_data["game"]

        # Статистика в recap
        recap["total_episodes"] += len(session_data["episodes"])
        recap["total_sessions"] += 1


        game_data[game]["total_episodes"] += len(session_data["episodes"])
        game_data[game]["total_sessions"] += 1

    recap["games"] = game_data

    return recap


        

if __name__ == "__main__":
    sessions = load_sessions(start_date=1764529201)

    recap = make_month_recap("22-09")
    
    print(recap)