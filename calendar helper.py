from collections import Counter

game_mapping = {
    'c': 'Cyberpunk',
    'g': 'Grand Theft Auto Online',
    's': 'SnowRunner',
    'f': 'Fallout 3',
    'b': 'Bully',
    'p': 'Prototype',
    'l': 'Life Is Strange: True Colors',
    'R': 'RAGE 2',
    't': 'Terraria: Calamity'
    # Добавьте остальные игры и их буквы здесь
}

# Открываем файл для чтения
with open("games.txt", "r") as file:
    # Инициализируем пустой массив month
    month = []

    # Инициализируем временный массив для хранения дней недели
    week_days = []

    # Счетчик для контроля количества дней в неделе
    day_counter = 0

    # Читаем каждую строку из файла
    for line in file:
        # Удаляем символы новой строки и лишние пробелы
        line = line.strip()

        # Если строка не пустая, разбиваем её на отдельные игры и добавляем их в день месяца
        if line:
            day_games = [game for game in line]
        else:
            # Если строка пустая, значит в этот день не было игр
            day_games = []

        # Добавляем день месяца в временный массив дней недели
        week_days.append(day_games)
        day_counter += 1

        # Если набралось 7 дней, создаем новую неделю и сбрасываем счетчик
        if day_counter == 7:
            month.append(week_days)
            week_days = []
            day_counter = 0

# Проходим по каждому элементу массива month и заменяем букву на название игры
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
# Собираем все игры в список
all_games = [game for week in month for day in week for game in day]

# Подсчитываем количество каждой игры
game_counter = Counter(all_games)

print("Количество различных игр:", len(game_counter))
# for game, count in game_counter.items():
#     print(f"{game}: {count}")
print('-'*20)

# Количество дней с одной, двумя и тремя играми
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