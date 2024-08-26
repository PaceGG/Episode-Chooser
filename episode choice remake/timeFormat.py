"""
Функции:
- time_format: Возвращает строку в формате 02:34 (134)
- short_date_format: Возвращает строку в формате dd.mm.yy HH:MM
- pc_date_format: Возвращает строку в формате времени компьютера
"""

from math import ceil
from time import strftime, localtime

def time_format(minutes):
    """ 134 -> 02:34 (134) """
    minutes = ceil(minutes)
    if minutes > 60: return f"{minutes//60:02}:{minutes%60:02} ({minutes})"
    return f"({ceil(minutes)})"

def short_date_format(time):
    """ dd.mm.yy HH:MM """
    return strftime("%d.%m.%y %H:%M", localtime(time))

months = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]
days_of_week = [
    "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"
]

def pc_date_format(t):
    day = strftime("%d", localtime(t))
    month = months[int(strftime("%m", localtime(t))) - 1]
    weekday = days_of_week[localtime().tm_wday]
    year = strftime("%y", localtime(t))
    hour_minute = strftime("%H:%M", localtime(t))
    
    return f"{hour_minute}, {day} {month} {weekday} {year}г."

if __name__ == "__main__":
    pass