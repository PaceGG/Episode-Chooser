from random import randint
import os
from os.path import *
from time import *
from datetime import datetime
from math import ceil
import win32api
import win32gui
import requests
import json


with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)

# Переключение раскладки клавиатуры на английскую
def setEngLayout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return(result)

def send_image(bot_token, chat_id, image_path, caption=None):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    params = {'chat_id': chat_id, 'caption': caption}
    response = requests.post(url, files=files, data=params)
    return response.json

# 396
def edit_telegram_message(bot_token, chat_id, message_id, new_text):
    """
    Редактирует сообщение в Telegram по его ID.
    
    :param bot_token: Токен бота Telegram
    :param chat_id: ID чата
    :param message_id: ID сообщения, которое нужно отредактировать
    :param new_text: Новый текст сообщения
    :return: Ответ API Telegram
    """
    url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": new_text
    }
    
    response = requests.post(url, params=params)
    
    return response.json()

bot_token = '6739691945:AAG_FoagOmFd-GUFpFwriEeTFgma-rwjGx8'
chat_id = '-1002035302407'

# DATA

# Официальные назцания игр
first_game_name = data['showcase'][0]['name'].replace(":", "")
second_game_name = data['showcase'][1]['name'].replace(":", "")
third_game_name = 'SnowRunner [ng+]'

first_game_short_name = data['showcase'][0]['shortName']
second_game_short_name = data['showcase'][1]['shortName']
third_game_short_name = 'SR'

# create files:
# ng.png in icons_new folder
# run mkdir.py

# Telegram captions
first_game_extra_caption = ""
second_game_extra_caption = ""

# Пути к файлам видео
first_game_video = first_game_name
first_game_video_extra = ""

second_game_video = second_game_name
second_game_video_extra = ""



# Programm
# Путри к играм
first_game_path = "C:\\Users\\yura3\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Play GUNSLINGER Mod.lnk"
second_game_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\TileIconify\Custom Shortcuts\Dead Space\Dead Space.lnk"
third_game_path = 'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'

# Пути к файлам видео
first_folder_name = "D:/Program Files/Shadow Play/" + first_game_video + "/previews/" + first_game_video_extra
second_folder_name = "D:/Program Files/Shadow Play/" + second_game_video + "/previews/" + second_game_video_extra
third_folder_name = 'D:/Program Files/Shadow Play/SnowRunner/previews/'

# Пути к иконкам игр
first_game_icon = f"D:\\Program Files\\HTML\\Games\\icons_new\\{first_game_name}.png"
second_game_icon = f"D:\\Program Files\\HTML\\Games\\icons_new\\{second_game_name}.png"
third_game_icon = f"D:\\Program Files\\HTML\\Games\\icons_new\\{third_game_name}.png"


def create_game_structure(game_name, base_directory):
    game_path = os.path.join(base_directory, game_name)
    os.makedirs(game_path, exist_ok=True)
    previews_path = os.path.join(game_path, "previews")
    os.makedirs(previews_path, exist_ok=True)
    episodes_log_path = os.path.join(previews_path, "episodes log.txt")
    with open(episodes_log_path, 'w'):
        pass
    episodes_time_path = os.path.join(previews_path, "episodes time.txt")
    with open(episodes_time_path, 'w') as f:
        f.write("0\n0")
        
    print("Директории созданы")

def icon_rename(game_name):
    directory = "D:\\Program Files\\HTML\\Games\\icons_new"
    variants = ["ng", "new_game", "new game"]
    
    for variant in variants:
        full_path = os.path.join(directory, f"{variant}.png")
        if os.path.exists(full_path):
            new_full_path = os.path.join(directory, f"{game_name}.png")
            os.rename(full_path, new_full_path)
            print(f"Файл '{full_path}' переименован в '{new_full_path}'")
            return
    print("Ни один из файлов для переименовывания не найден")

# Время игр
def get_time(dir):
    dir += "/episodes time.txt"

    with open(dir, 'r') as f:
        time = int(f.readline())
        my_time = f.readline()

        if "," in my_time:
            total_time = 0
            my_time = my_time.split(",")
            for time in my_time:
                if ":" in time:
                    time = time.split(":")
                    time = int(time[0]) * 60 + int(time[1])
                else:
                    time = int(time)
                total_time += time
        my_time = total_time
        if my_time == 0:
            return time
        else:
            extra_time = my_time - time
            time = 120 - extra_time
    
    with open(dir, 'w') as f:
        f.write(f"{time}\n0")
    
    return time

# Номер последней серии
def get_last_episode(dir):
    dir += "/episodes log.txt"

    try: open(dir)
    except: 
        if dir.find(first_game_name) != -1:
            game_name = first_game_name
        if dir.find(second_game_name) != -1:
            game_name = second_game_name

        icon_rename(game_name)
        base_directory = "D:/Program Files/Shadow Play"
        create_game_structure(game_name, base_directory)
        print("\n"*20)

    with open(dir, 'r') as f:
        lines = f.readlines()

    if lines:
        last_ep, real_ep = lines[-1].split()
        last_ep = int(last_ep)
        if '-' in real_ep:
            real_ep = int(real_ep[real_ep.find('-')+1:real_ep.find(')')])
        else:
            real_ep =  int(real_ep[real_ep.find('(')+1:real_ep.find(')')])
    else:
        last_ep = 0
        real_ep = 0

    return last_ep, real_ep

first_game_last_ep, first_game_last_ep_real = get_last_episode(first_folder_name)
second_game_last_ep, second_game_last_ep_real = get_last_episode(second_folder_name)
third_game_last_ep, third_game_last_ep_real = get_last_episode(third_folder_name)

first_game_time = get_time(first_folder_name)
second_game_time = get_time(second_folder_name)
third_game_time = get_time(third_folder_name)

# Time equalization
first_game_time_penalty = 120 - first_game_time
second_game_time_penalty = 120 - second_game_time
penalty_min = min(first_game_time_penalty, second_game_time_penalty)
first_game_time += penalty_min
second_game_time += penalty_min

first_game_time_dir = first_folder_name + "episodes time.txt"
second_game_time_dir = second_folder_name + "episodes time.txt"
third_game_time_dir = third_folder_name + "episodes time.txt"
with open(first_game_time_dir, 'w') as f:
    f.write(f"{first_game_time}\n0")
with open(second_game_time_dir, 'w') as f:
    f.write(f"{second_game_time}\n0")

with open("D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt", 'r') as f:
    games_for_sr_counter = int(f.readline())

if third_game_time <= 0:
    with open(third_game_time_dir, 'w') as f:
        f.write(f"{120 + third_game_time}\n0")
    with open("D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt", 'w') as f:
        f.write(f"{games_for_sr_counter+5}\n")


def time_format(minutes):
    minutes = ceil(minutes)
    if minutes > 60: return f"{minutes//60:02}:{minutes%60:02} ({minutes})"
    return str(ceil(minutes))

if first_game_time.is_integer(): first_game_time = int(first_game_time)
if second_game_time.is_integer(): second_game_time = int(second_game_time)

first_game_total_length = time_format(first_game_time)
second_game_total_length = time_format(second_game_time)
third_game_total_length = time_format(third_game_time)
if first_game_time != 120: first_game_time = f"::({time_format(first_game_time/3) + " / "}{time_format(first_game_time/3*2) + " / "}{time_format(first_game_time)})::"
else: first_game_time = ""
if second_game_time != 120: second_game_time = f"::({time_format(second_game_time/3) + " / "}{time_format(second_game_time/3*2) + " / "}{time_format(second_game_time)})::"
else: second_game_time = ""
if third_game_time != 120: third_game_time = f"::({time_format(third_game_time)})::"
else: third_game_time = ""

first_game_length = first_game_time
second_game_length = second_game_time
third_game_length = third_game_time


# Game caption
if first_game_extra_caption != "": first_game_extra_caption = ": "+first_game_extra_caption
if second_game_extra_caption != "": second_game_extra_caption = ": "+second_game_extra_caption

first_game_caption = f"{first_game_name+first_game_extra_caption} № {first_game_last_ep_real+1}-{first_game_last_ep_real+3}:\n• \n• \n• "
second_game_caption = f"{second_game_name+second_game_extra_caption} № {second_game_last_ep_real+1}-{second_game_last_ep_real+3}:\n• \n• \n• "
third_game_caption = f"{third_game_name} № {third_game_last_ep_real+1}:\n• "

    
# Episodes count
first_episodes = first_game_last_ep*3
second_episodes = second_game_last_ep*3


# Game date

#first game
first_episodes_list = os.listdir(first_folder_name)
first_game_dates = []

for i in first_episodes_list:
    if i.endswith('.jpg') and not('s' in i):
        first_game_dates.append(int(getctime(f'{first_folder_name}\\{i}')))

first_date = int(getctime(f'{first_folder_name}'))

#second game
second_episodes_list = os.listdir(second_folder_name)
second_game_dates = []

for i in second_episodes_list:
    if i.endswith('.jpg') and not('s' in i):
        second_game_dates.append(int(getctime(f'{second_folder_name}\\{i}')))

second_date = int(getctime(f'{second_folder_name}'))

# third game
third_episodes_list = os.listdir(third_folder_name)
third_game_dates = []

for i in third_episodes_list:
    if i.endswith('.jpg'):
        third_game_dates.append(int(getctime(f'{third_folder_name}\\{i}')))

if len(third_game_dates) > 0:
    third_date = max(third_game_dates)
else:
    third_date = 0
    
current_date = int(time())


# earlier & start_from
    
if first_date > second_date:
    earlier = second_game_name
    later = first_game_name
else:
    earlier = first_game_name
    later = second_game_name

if first_episodes == 0 or second_episodes == 0:
    with open('start_from.txt', 'w') as start_from:
        if first_episodes == 0:
            start_from.write(str(second_episodes))
        if second_episodes == 0:
            start_from.write(str(first_episodes))

with open('start_from.txt', 'r') as file:
    start_from = int(file.readline())


if earlier == first_game_name:
    first_episodes -= start_from
if earlier == second_game_name:
    second_episodes -= start_from
    
# force earlier
earlier_force = False
if earlier_force:
    earlier = second_game_name
    

# force number of episodes
force_flag = False

if force_flag:
    first_episodes = 6
    second_episodes = 9


# Game list/today
  
more_game = abs(first_episodes-second_episodes)//3 + 1

if first_episodes > second_episodes:
    first_chanse = 1
    second_chanse = more_game
else:
    first_chanse = more_game
    second_chanse = 1
    
game_list = []

for i in range(first_chanse):
    game_list.append(first_game_name)
for i in range(second_chanse):
    game_list.append(second_game_name)

def check_frequency():
    with open("games_log.txt", 'rb') as f:
        # Сначала переместимся в конец файла
        f.seek(0, 2)
        end_pos = f.tell()
        
        # Теперь будем читать файл с конца, начиная с позиции end_pos
        buffer_size = 1024
        buffer = b''
        pos = end_pos
        lines = []
        
        while pos > 0 and len(lines) < 4:
            # Определяем текущую позицию для чтения
            start_pos = max(pos - buffer_size, 0)
            f.seek(start_pos)
            buffer = f.read(pos - start_pos) + buffer
            pos = start_pos
            
            # Разбиваем буфер на строки
            lines = buffer.split(b'\n')[-4:]
            buffer = lines[0]
            
        last_three_games = [line.decode('utf-8')[:-1] for line in lines if line]

        if len(set(last_three_games)) > 1:
            return game_list[randint(0,len(game_list)-1)], "random", last_three_games
        elif len(set(last_three_games)) == 1:
            popular_game = last_three_games[0]
            if popular_game == first_game_name:
                unpopular_game = second_game_name
            else:
                unpopular_game = first_game_name
            return unpopular_game, "force", last_three_games
today, today_method, last_three_games = check_frequency()
    

# Game_time

first_time_folder = os.listdir(first_folder_name+'/../')
first_game_time = []

for i in first_time_folder:
    if i.endswith('.txt'):
        first_game_time.append(i)
for i in range(len(first_game_time)):
    s = ''
    for x in first_game_time[i]:
        if x.isdigit():
            s += x
        else:
            break
    first_game_time[i] = s
for i in range(first_game_time.count('')):
    first_game_time.remove('')
    
    
second_time_folder = os.listdir(second_folder_name+'/../')
second_game_time = []

for i in second_time_folder:
    if i.endswith('.txt'):
        second_game_time.append(i)
for i in range(len(second_game_time)):
    s = ''
    for x in second_game_time[i]:
        if x.isdigit():
            s += x
        else:
            break
    second_game_time[i] = s
for i in range(second_game_time.count('')):
    second_game_time.remove('')

    
# Output
def addEp(dir):
    dir += "/episodes log.txt"

    with open(dir, 'r') as f:
        lines = f.readlines()

    if lines:
        last_ep, real_ep = lines[-1].split()
        last_ep = int(last_ep)
        if '-' in real_ep:
            real_ep = int(real_ep[real_ep.find('-')+1:real_ep.find(')')])
        else:
            real_ep =  int(real_ep[real_ep.find('(')+1:real_ep.find(')')])
    else:
        last_ep = 0
        real_ep = 0

    with open(dir, 'a') as f:
        if 'SnowRunner' in dir:
            f.write(f"{str(last_ep+1)} ({last_ep+1})\n")
        else:
            f.write(f"{str(last_ep+1)} ({real_ep+1}-{real_ep+3})\n")

def sr_db_edit():
    dir = "D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt"

    with open(dir, 'w') as f:
        f.write(str(games_for_sr_counter - 1))

def sr_db_clear():
    dir = "D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt"

    with open(dir, 'w') as f:
        f.write('5')

def edit_tg_info_message():
    if first_episodes == second_episodes == 0:
        sr_info_add_message = "• SR: 4"
        if earlier == second_game_name:
            add_message = f"• {second_game_short_name}: 2"
        elif earlier == first_game_name:
            add_message = f"• {first_game_short_name}: 2"

        edit_telegram_message(bot_token, chat_id, 396, f"""
{sr_info_add_message}
{add_message}
    """)
        return

    first_game_count = game_list.count(first_game_name)
    second_game_count = game_list.count(second_game_name)

    if len(set(last_three_games[1:] + [today])) == 1:
        popular_game = last_three_games[-1]
        if popular_game == first_game_short_name:
            unpopular_game = second_game_short_name
        else:
            unpopular_game = first_game_short_name
        force_info_message = f"• Force: {unpopular_game}"
    else:
        force_info_message = ""

    if first_game_count == second_game_count == 1:
        if today == first_game_name: second_game_count += 1
        if today == second_game_name: first_game_count += 1
    elif first_game_count > 1:
        if today == first_game_name: first_game_count -= 1
        if today == second_game_name: first_game_count += 1
    elif second_game_count > 1:
        if today == first_game_name: second_game_count += 1
        if today == second_game_name: second_game_count -= 1

    if first_game_count == second_game_count == 1: add_message = f"• Шансы равны"
    if first_game_count > 1: add_message = f"• {first_game_short_name}: {first_game_count}"
    if second_game_count > 1: add_message = f"• {second_game_short_name}: {second_game_count}"


    if games_for_sr_counter - 1 != 0: sr_info_add_message = f"• SR: {games_for_sr_counter - 1}"
    else: sr_info_add_message = f"• Сегодня SnowRunner!!! • {third_game_short_name}: {third_game_total_length}" if third_game_length else "• Сегодня SnowRunner!!!"

    length_message = ""
    length_message += f"• {first_game_short_name}: {first_game_length}\n" if first_game_length else ""
    length_message += f"• {second_game_short_name}: {second_game_length}\n" if second_game_length else ""
    length_message += f"• {third_game_short_name}: {third_game_total_length}\n" if third_game_length else ""


    edit_telegram_message(bot_token, chat_id, 396, f"""
{sr_info_add_message}
{force_info_message}
{add_message}
{length_message}
    """)

def add_game_log(game):
    with open("games_log.txt", "a") as f:
        f.write(f"{game}\n")

def snowrunner_updater():
    updater_path = f"D:/Program Files/Shadow Play/SnowRunner/update.txt"
    if os.path.exists(updater_path): os.remove(updater_path)
    else:
        with open(updater_path, 'w') as f:
            pass

def run_game(x):
    # os.startfile(f'"{"D:/Program Files/obs-studio/bin/64bit/obs64.exe"}"')
    if x == first_game_name:
        print(f"{first_game_name}{f": {first_game_length}" if first_game_length else ""}")
        send_image(bot_token, chat_id, first_game_icon, first_game_caption)
        addEp(first_folder_name)
        add_game_log(first_game_name)
        os.startfile(first_game_path)
    if x == second_game_name:
        print(f"{second_game_name}{f": {second_game_length}" if second_game_length else ""}")
        send_image(bot_token, chat_id, second_game_icon, second_game_caption)
        addEp(second_folder_name)
        add_game_log(second_game_name)
        os.startfile(second_game_path)
    if x == 'SR':
        print(f"{third_game_name}{f": {third_game_length}" if third_game_length else ""}")
        send_image(bot_token, chat_id, third_game_icon, third_game_caption)
        addEp(third_folder_name)
        os.startfile(third_game_path)
    sr_db_edit()
    edit_tg_info_message()
        

def run_random_game():
    if first_episodes == 0 and second_episodes == 0:
        sr_db_clear()
        if earlier == second_game_name:
            run_game(first_game_name)
        if earlier == first_game_name:
            run_game(second_game_name)
    # elif not(first_game_week and second_game_week and third_game_week):
    elif games_for_sr_counter != 0:
        run_game(today)
    else:
        run_game('SR')

edit_text = ""
def add_edit_text(string):
    global edit_text
    edit_text += string + "\n"

def print_game_list_newFormat():
    global game_list

    first_game_count = game_list.count(first_game_name)
    second_game_count = game_list.count(second_game_name)

    if today_method == "force":
        print(f"Force: {today}\n")
        if today == first_game_name: add_edit_text(f"• Force: {first_game_short_name}")
        if today == second_game_name: add_edit_text(f"• Force: {second_game_short_name}")

    if first_game_count == second_game_count == 1:
        print("Шансы равны")
        add_edit_text("Шансы равны")
    elif first_game_count > 1:
        print(f'{first_game_name}: {first_game_count}')
        add_edit_text(f"• {first_game_short_name}: {first_game_count}")
    elif second_game_count > 1:
        print(f'{second_game_name}: {second_game_count}')
        add_edit_text(f"• {second_game_short_name}: {second_game_count}")

    print()
    if first_game_length: print(f"{first_game_name} {first_game_length}")
    if second_game_length: print(f"{second_game_name} {second_game_length}")
    if first_game_length or second_game_length or third_game_length: add_edit_text("")
    add_edit_text(f"• {first_game_short_name}: {first_game_total_length}") if first_game_length else ""
    add_edit_text(f"• {second_game_short_name}: {second_game_total_length}") if second_game_length else ""
    add_edit_text(f"• {third_game_short_name}: {third_game_total_length}") if third_game_length else ""

def print_info():
    global games_for_sr_counter

    if games_for_sr_counter == 1:
        ep_prefix = 'я'
    elif 1 < games_for_sr_counter < 5:
        ep_prefix = 'и'
    else:
        ep_prefix = 'й'
    
    if first_episodes == second_episodes == 0:
        games_for_sr_counter = 5
        ep_prefix = 'й'

    if games_for_sr_counter > 0:
        print(f"До SnowRunner'a ещё {games_for_sr_counter} сери{ep_prefix}")
        print()
        add_edit_text(f"• SR: {games_for_sr_counter}")
    else:
        print(f"Сегодня SnowRunner: {third_game_length}")
        print()
        add_edit_text("• Сегодня SnowRunner!!!")
        add_edit_text(f"• {third_game_short_name}: {third_game_total_length}") if third_game_length else ""
        
        
    # print(today)
    print_game_list_newFormat()
    
# 1 для запуска игры, 0 для вывода списка игр
run_flag = 1

setEngLayout()

print_info()
edit_telegram_message(bot_token, chat_id, 396, edit_text)

if run_flag:
    print("\n"*10)
    confirm = input()
    run_random_game()