from collections import Counter

game_mapping = {
    "Pt" : "Prototype",
    "Bl": "Bully: Scholarship Edition",
    "F3" : "Fallout 3",
    "Cp" : "Cyberpunk 2077",
    "Gt0" : "Grand Theft Auto Online",
    'Sw' : "Saints Row",
    "Re5": "Resident Evil 5",
    'Re6' : "Resident Evil 6",
    'Re7': "Resident Evil 7",
    'Re8' : "Resident Evil Village",
    'Sr' : "Snow Runner",
    "St" : "S.T.A.L.K.E.R.: Lost Alpha DC",
    "Sc": "S.T.A.L.K.E.R.: Clear Sky",
    "Sp": "S.T.A.L.K.E.R.: Call of Pripyat",
    "So": "Soma",
    "Cu": "Cuphead",
    "Ow": "Outer Wilds",
    "Ls2": "Life Is Strange 2",
    "Ah": "Atomic Heart",
    "Ds": "Dead Space",
    "Fv": "Fallout: New Vegas",
}

with open("games.txt", "r") as file:
    month = []
    week_days = []
    day_counter = 0
    for line in file:
        line = line.strip()
        day_games = []
        i = 0
        while i < len(line):
            if line[i].isupper() and i + 1 < len(line) and line[i + 1].islower():
                game = line[i:i+2]
                i += 2
                while i < len(line) and line[i].isdigit():
                    game += line[i]
                    i += 1
                day_games.append(game)
            else:
                game = line[i]
                i += 1
                while i < len(line) and line[i].isdigit():
                    game += line[i]
                    i += 1
                day_games.append(game)
        week_days.append(day_games)
        day_counter += 1
        if day_counter == 7:
            month.append(week_days)
            week_days = []
            day_counter = 0

    if week_days:
        month.append(week_days)

for week in month:
    for day in week:
        for i, game in enumerate(day):
            if game in game_mapping:
                day[i] = game_mapping[game]

# 4. Общее количество игр
total_games = sum(len(day) for week in month for day in week)
print("Общее количество игр:", total_games)

# 1. Количество игр в каждую неделю
for i, week in enumerate(month):
    print(f"Количество игр в {i+1} неделю: {sum(len(day) for day in week)}")
print('-'*20)

# 2. Неделя с наибольшим/наименьшим количеством игр
max_games_week_index = max(range(len(month)), key=lambda x: sum(len(day) for day in month[x]))
min_games_week_index = min(range(len(month)), key=lambda x: sum(len(day) for day in month[x]))
max_games_week = month[max_games_week_index]
min_games_week = month[min_games_week_index]
print(f"Самая длинная неделя:  {max_games_week_index + 1} | {sum(len(day) for day in max_games_week)}")
print(f"Самая короткая неделя: {min_games_week_index + 1} | {sum(len(day) for day in min_games_week)}")
print('-'*20)

# 3. Количество различных игр и их количество
all_games = [game for week in month for day in week for game in day]

game_counter = Counter(all_games)

print("Количество различных игр:", len(game_counter))
for game, count in sorted(game_counter.items()):
    print(f"{game}: {count}")
print('-'*20)

games_per_day_counter = Counter(len(day) for week in month for day in week)
days_with_one_game = games_per_day_counter[1]
days_with_two_games = games_per_day_counter[2]
days_with_three_games = games_per_day_counter[3]

print("Количество дней в которые 1 игра:", days_with_one_game)
print("Количество дней в которые 2 игры:", days_with_two_games)
print("Количество дней в которые 3 игры:", days_with_three_games)
print('-'*20)

# 5. Самая популярная игра
most_common_game = Counter(all_games).most_common(1)[0][0]
print("Самая популярная игра:", most_common_game)
