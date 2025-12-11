import json
from ai_recap import make_all_time_recap, make_month_recap, make_year_recap, print_all_time_recap, print_recap, print_year_recap

def convert_sets_to_lists(obj):
    """Рекурсивно преобразует все множества в списки"""
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    else:
        return obj

with open(r"D:\Program Files\HTML\Episode-Chooser\react-remake\public\sessions.json", 'r', encoding='utf-8') as f:
    sessions = json.load(f)

month_recap = make_month_recap("25-11", sessions)

# Преобразуем все множества в списки
month_recap_serializable = convert_sets_to_lists(month_recap)

with open("month-recap-25-11.json", "w", encoding='utf-8') as f:
    json.dump(month_recap_serializable, f, ensure_ascii=False, indent=2)