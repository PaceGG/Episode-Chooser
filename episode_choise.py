from random import randint
import os
from os.path import *
from time import *
from datetime import datetime
import win32api
import win32gui
import requests
import json


with open("react-remake/db.json", encoding="utf-8") as f:
    data = json.load(f)



test = 0

if test == 1:
    print(data['showcase'][0]['name'])
    print(data['showcase'][1]['name'])
    exit(0)


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
first_game_name = data['showcase'][0]['name']
second_game_name = data['showcase'][1]['name']
third_game_name = 'SnowRunner'

# Название ярлыков
first_game_ico = "Cuphead"
second_game_ico = 'ladc'

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
first_game_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Life Is Strange 2\\Life Is Strange 2.lnk"
second_game_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\ladc.lnk"
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


# Когда будет снов ранер new
with open("D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt") as f:
    times = [int(time) for time in f.readlines()]

games_for_sr_counter = len(times)


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

today = game_list[randint(0,len(game_list)-1)]
    

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

    with open(dir, 'r+') as f:
        times = [int(time) for time in f.readlines()]
    
        for_sr = 5 - len(times)

        if for_sr > 0:
            f.write(f'{str(int(time()))}\n')
        if for_sr == 0:
            with open(dir, 'w') as ff:
                f.write('')

def sr_db_clear():
    dir = "D:/Program Files/Shadow Play/SnowRunner/previews/snowrunner counter.txt"

    with open(dir, 'w') as f:
        f.write('')

def edit_tg_info_message():
    first_game_count = game_list.count(first_game_name)
    second_game_count = game_list.count(second_game_name)

    if first_game_count == second_game_count == 1:
        if today == first_game_name: second_game_count += 1
        if today == second_game_name: first_game_count += 1
    elif first_game_count > 1:
        if today == first_game_name: first_game_count -= 1
        if today == second_game_name: first_game_count += 1
    elif second_game_count > 1:
        if today == first_game_name: second_game_count += 1
        if today == second_game_name: second_game_count -= 1

    if first_game_count == second_game_count == 1: add_message = f"• {first_game_name}: {first_game_count}" + "\n" + f"• {second_game_name}: {second_game_count}"
    if first_game_count > 1: add_message = f"• {first_game_name}: {first_game_count}"
    if second_game_count > 1: add_message = f"• {second_game_name}: {second_game_count}"


    if 5 - games_for_sr_counter - 1 != 0: sr_info_add_message = f"• SR: {5 - games_for_sr_counter - 1}"
    else: sr_info_add_message = "• Сегодня SnowRunner!!!"


    edit_telegram_message(bot_token, chat_id, 396, f"""
{sr_info_add_message}
{add_message}
    """)

def run_game(x):
    # os.startfile(f'"{"D:/Program Files/obs-studio/bin/64bit/obs64.exe"}"')
    if x == first_game_name:
        print(first_game_name)
        send_image(bot_token, chat_id, first_game_icon, first_game_caption)
        addEp(first_folder_name)
        os.startfile(first_game_path)
    if x == second_game_name:
        print(second_game_name)
        send_image(bot_token, chat_id, second_game_icon, second_game_caption)
        addEp(second_folder_name)
        os.startfile(second_game_path)
    if x == 'SR':
        print(third_game_name)
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
    elif games_for_sr_counter < 5:
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

    if first_game_count == second_game_count == 1:
        print(f"{first_game_name}: {first_game_count}")
        print(f'{second_game_name}: {second_game_count}')
        add_edit_text("Шансы равны")
        return
    if first_game_count > 1:
        print(f'{first_game_name}: {first_game_count}')
        add_edit_text(f"• {first_game_name}: {first_game_count}")
        return
    if second_game_count > 1:
        print(f'{second_game_name}: {second_game_count}')
        add_edit_text(f"• {second_game_name}: {second_game_count}")
        return

def print_info():
    global games_for_sr_counter

    games_to_sr_counter = 5 - games_for_sr_counter
        
    if games_to_sr_counter == 1:
        ep_prefix = 'я'
    elif 1 < games_to_sr_counter < 5:
        ep_prefix = 'и'
    else:
        ep_prefix = 'й'
    
    if first_episodes == second_episodes == 0:
        games_to_sr_counter = 5
        ep_prefix = 'й'

    if games_to_sr_counter > 0:
        print(f"До SnowRunner'a ещё {games_to_sr_counter} сери{ep_prefix}")
        add_edit_text(f"• SR: {5 - games_for_sr_counter}")
    else:
        print(f"Сегодня SnowRunner")
        add_edit_text("• Сегодня SnowRunner!!!")
        
        
    # print(today)
    print_game_list_newFormat()
    
# 1 для запуска игры, 0 для вывода списка игр
run_flag = 0

setEngLayout()

print_info()
edit_telegram_message(bot_token, chat_id, 396, edit_text)

if run_flag:
    print("\n"*10)
    confirm = input()
    run_random_game()