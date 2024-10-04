from pydata import pydata_load
from timeFormat import prev_month
import os
import PATHS

os.chdir(PATHS.repository)


log = pydata_load("game_log")["game_log"]

# date
prev_date = prev_month()
date = f"01 {prev_date[0]} {prev_date[1]}"

# popular_game
count = {}

for week in log:
    for day in week:
        for game in day:
            if game in count:
                count[game] += 1
            else:
                count[game] = 1

popular_game = max(count, key=count.get)

# number_of_games
number_of_games = sum(count.values())

# number_of_weeks
number_of_weeks = []

for week in log:
    week_count = 0
    for day in week:
        week_count += len(day)

    number_of_weeks.append(week_count)

number_of_weeks = str(number_of_weeks).replace("[","").replace("]","").replace(" ","").replace(",", "	")

# longest_week
longest_week = number_of_weeks.index(max(number_of_weeks))+1

# shortest_week
shortest_week = number_of_weeks.index(min(number_of_weeks[:-2]))+1

# different_games
games = list(count.keys())
different_games = len(games)

# statistics
statistics = f"{date}	{popular_game}	{number_of_games}	{number_of_weeks}	{longest_week}	{shortest_week}	{different_games}"


def save():
    statistics_filename = f"statistics {date}.txt"
    statistics_filename = os.path.join(PATHS.repository, statistics_filename)
    with open(statistics_filename, "w", encoding="utf-8") as f:
        f.write(statistics)

if __name__ == "__main__":
    save(statistics)