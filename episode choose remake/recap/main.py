import json

from ai_recap import make_all_time_recap, make_month_recap, make_year_recap, print_all_time_recap, print_recap, print_year_recap

with open(r"D:\Program Files\HTML\Episode-Chooser\react-remake\public\sessions.json", 'r', encoding='utf-8') as f:
        sessions = json.load(f)

year_recap = make_year_recap("24", sessions)

