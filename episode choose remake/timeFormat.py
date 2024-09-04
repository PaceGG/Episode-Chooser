"""
Функции форматирования:
- time_format: Возвращает строку в формате 02:34 (134)
- short_date_format: Возвращает строку в формате dd.mm.yy HH:MM
- pc_date_format: Возвращает строку в формате времени компьютера

Функции извлечения дат:
- calendar_position: Возвращает позицию даты в календаре [номер недели][номер дня]
- date_position: Возвращает позицию даты относительно начала месяца

- today: Возвращает текущую дату в unix формате

- get_day: Возвращает день месяца
- get_month: Возвращает месяц
- get_year: Возвращает год
- get_time: Возвращает время формата HH:MM

- end_of_month: Возвращает дату конца месяца
"""

from math import ceil
from time import strftime, localtime, mktime, strptime, time

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


def calendar_position(unix_timestamp):
    date_struct = localtime(unix_timestamp)
    day_of_week = date_struct.tm_wday
    first_day_of_month = localtime(mktime(strptime(f"{date_struct.tm_year}-{date_struct.tm_mon}-01", "%Y-%m-%d")))
    day_of_month = date_struct.tm_mday
    week_of_month = (day_of_month + first_day_of_month.tm_wday - 1) // 7

    return week_of_month, day_of_week

def date_position(unix_timestamp):
    day = get_day(unix_timestamp)

    if day % 7 == 0:
        week = day // 7 - 1
        wday = 7 - 1
    else:
        week = day // 7
        wday = day % 7 - 1

    return week, wday

def get_day(unix_timestamp=time()):
    return int(strftime("%d", localtime(unix_timestamp)))

def get_month(unix_timestamp=time()):
    return int(strftime("%m", localtime(unix_timestamp)))

def get_year(unix_timestamp=time()):
    return int(strftime("%Y", localtime(unix_timestamp)))

def get_time(unix_timestamp=time()):
    return strftime("%H:%M", localtime(unix_timestamp))

def last_day(unix_timestamp=time()):
    month = get_month(unix_timestamp)

    if month == 2 and get_year(unix_timestamp) % 4 != 0: return 28
    elif month == 2 and get_year(unix_timestamp) % 4 == 0: return 29
    elif month in [1, 3, 5, 7, 8, 10, 12]: return 31
    elif month in [4, 6, 9, 11]: return 30

def end_of_month(unix_time):
    struct_time = localtime(unix_time)
    
    if struct_time.tm_mon == 12:
        next_month = 1
        next_year = struct_time.tm_year + 1
    else:
        next_month = struct_time.tm_mon + 1
        next_year = struct_time.tm_year
    
    first_of_next_month = (next_year, next_month, 1, 0, 0, 0, 0, 0, struct_time.tm_isdst)
    first_of_next_month_unix = int(mktime(first_of_next_month))
    
    return first_of_next_month_unix - 1


def today():
    return int(time())

if __name__ == "__main__":

    # print(last_day(today()))
    # print(end_of_month(today())
    # print(date_position(1724739895))
    print(date_position(today()))

    pass