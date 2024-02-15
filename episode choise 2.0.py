from random import randint
from os import *
from os.path import getctime
from time import *
from datetime import datetime
import win32api
import win32gui
import requests


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

bot_token = '6739691945:AAG_FoagOmFd-GUFpFwriEeTFgma-rwjGx8'
chat_id = '-1002035302407'
image_path = 'testimg.png'


# DATA

# Официальные назцания игр
firs_game_name = 'Grand Theft Auto Online'
second_game_name = 'Fallout 3'
third_game_name = 'SnowRunner'

game_name = [
"Grand Theft Auto Online",
"Fallout 3",
"SnowRunner"]

# Краткие названия игр
first_game = 'gta'
second_game = 'fallout'
third_game = 'SR'

game = [
"gta",
"fallout",
"SR"
]

# название ярлыков
first_game_ico = "PlayGTAV"
second_game_ico = 'Fallout3'

game_ico = [
"PlayGTAV",
"Fallout3"
]

# Пути к файлам видео
first_game_video = "Grand Theft Auto V"
first_game_video_extra = "gta online"

second_game_video = second_game_name
second_game_video_extra = ""

game_video = [
"Grand Theft Auto V",
second_game_name,
]

game_video_extra = [
"gta online",
""
]




# Programm
# Удаление ":" из названия файла
# Первое видео
first_game_video_temp = ""
for i in range(len(first_game_video)):
    if first_game_video[i] != ':':
        first_game_video_temp += first_game_video[i]
    else:
        first_game_video_temp += ' '
first_game_video = first_game_video_temp
# Второе видео
second_game_video_temp = ""
for i in range(len(second_game_video)):
    if second_game_video[i] != ':':
        second_game_video_temp += second_game_video[i]
    else:
        second_game_video_temp += ' '
second_game_video = second_game_video_temp





# Путри к играм
first_game_path = 'C:\\Users\\yura3\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\' + first_game_ico + '.lnk'
second_game_path = 'C:\\Users\\yura3\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\' + second_game_ico + ".lnk"
third_game_path = 'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'

# Пути к файлам видео
first_folder_name = "D:/Program Files/Shadow Play/" + first_game_video + "/previews/" + first_game_video_extra
second_folder_name = "D:/Program Files/Shadow Play/" + second_game_video + "/previews/" + second_game_video_extra
third_folder_name = 'D:\Program Files\Shadow Play\SnowRunner\previews'

# Пути к иконкам игр
first_game_icon = f"D:\Program Files\HTML\Games\icons_new\{firs_game_name}.png"
second_game_icon = f"D:\Program Files\HTML\Games\icons_new\{second_game_name}.png"
third_game_icon = f"D:\Program Files\HTML\Games\icons_new\{third_game_name}.png"

# Номер последней серии
# Для первой игры


# Telegram captions
first_game_caption = f"{firs_game_name} №"

    
# Episodes count

first_episodes = 0
second_episodes = 0

for root, dirs, files in walk(first_folder_name):
    for file in files:
        if(file.endswith(".jpg")) and not('f' in file.lower()):
            first_episodes += 1
            
            
for root, dirs, files in walk(second_folder_name):
    for file in files:
        if(file.endswith(".jpg")) and not('f' in file.lower()):
            second_episodes += 1
            

# Game date

#first game
first_episodes_list = listdir(first_folder_name)
first_game_dates = []

for i in first_episodes_list:
    if i.endswith('.jpg') and not('s' in i):
        first_game_dates.append(int(getctime(f'{first_folder_name}\\{i}')))

first_date = int(getctime(f'{first_folder_name}'))

#second game
second_episodes_list = listdir(second_folder_name)
second_game_dates = []

for i in second_episodes_list:
    if i.endswith('.jpg') and not('s' in i):
        second_game_dates.append(int(getctime(f'{second_folder_name}\\{i}')))

second_date = int(getctime(f'{second_folder_name}'))

# third game
third_episodes_list = listdir(third_folder_name)
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

sr_start_count = max(max(third_game_dates),int(getctime(first_folder_name)),int(getctime(second_folder_name)))

games_for_sr_counter = 0

for game in first_game_dates:
    if game > sr_start_count:
        games_for_sr_counter += 1
for game in second_game_dates:
    if game > sr_start_count:
        games_for_sr_counter += 1

        
# Когда будет снов ранер old
week = 5*24*60*60

#dates force
dates_force_flag = False
if dates_force_flag:
    #first date force
    first_date_force_flag = False
    if first_date_force_flag:
        first_date = 1690209416

    #second date force
    second_date_force_flag = False
    if second_date_force_flag:
        second_date = 0
        
    #third date force
    third_date_force_flag = False
    if third_date_force_flag:
        third_date = 1689259016
    

value = datetime.fromtimestamp(max(first_date,second_date,third_date)+week)
sr_date = value.strftime('%d.%m.%Y %H:%M:%S')



sr_for = max(first_date,second_date,third_date)+week - current_date

if sr_for < 0:
    sr_for = 'Должен начаться SnowRunner'
else:
    sr_for = f'{sr_for//86400} день, {sr_for-(sr_for//6)} часов, {sr_for//60} минут, {sr_for%60} секунд'

first_game_date = current_date - first_date
second_game_date = current_date - second_date
third_game_date = current_date - third_date


if first_game_date > week:
    first_game_week = True
else:
    first_game_week = False

if second_game_date > week:
    second_game_week = True
else:
    second_game_week = False
    
if third_game_date > week:
    third_game_week = True
else:
    third_game_week = False


# earlier & start_from            
if first_date > second_date:
    earlier = second_game
else:
    earlier = first_game
    


# if earlier == first_game:
#     first_episodes -= start_from
# if earlier == second_game:
#     second_episodes -= start_from
    
# force earlier
earlier_force = False
if earlier_force:
    earlier = second_game
    


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
    game_list.append(first_game)
for i in range(second_chanse):
    game_list.append(second_game)

today = game_list[randint(0,len(game_list)-1)]
    

# Game_time

first_time_folder = listdir(first_folder_name+'/../')
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
    
    
second_time_folder = listdir(second_folder_name+'/../')
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

def time_convert(game_time):
    if len(game_time) == 1:
        print(f'Time: {game_time[0]}')
    elif len(game_time) > 1:
        print('Time:')
        print(*game_time,sep='\n')

def run_game(x):
    if x == first_game:
        print(firs_game_name)
        send_image(bot_token, chat_id, first_game_icon, caption="Это ваша картинка!")
        time_convert(first_game_time)
        system(f'"{first_game_path}"')
    if x == second_game:
        print(second_game_name)
        send_image(bot_token, chat_id, second_game_icon, caption="Это ваша картинка!")
        time_convert(second_game_time)
        system(f'"{second_game_path}"')
    if x == 'SR':
        print(third_game_name)
        send_image(bot_token, chat_id, third_game_icon, caption="Это ваша картинка!")
        system(f'"{third_game_path}"')
        

def run_random_game():
    if first_episodes == 0 and second_episodes == 0:
        if earlier == second_game:
            run_game(first_game)
        if earlier == first_game:
            run_game(second_game)
    # elif not(first_game_week and second_game_week and third_game_week):
    elif games_for_sr_counter < 15:
        run_game(today)
    else:
        run_game('SR')
        
def print_game_list():
    print(game_list)
    
    
# 1 для запуска игры, 0 для вывода списка игр
run_flag = 1

setEngLayout()

if run_flag == 1:
    run_random_game()
else:
    # print(f'SnowRunner будет после {sr_date}.')
    
    games_for_sr_counter = 5-games_for_sr_counter//3
    
    if games_for_sr_counter == 1:
        ep_prefix = 'я'
    elif 1 < games_for_sr_counter < 5:
        ep_prefix = 'и'
    else:
        ep_prefix = 'й'
    
    # print(games_for_sr_counter)
    
    
    if games_for_sr_counter > 0:
        print(f"До SnowRunner'a ещё {games_for_sr_counter} сери{ep_prefix}")
    else:
        print(f'Сегодня SnowRunner')
        
    # print(today)
    print_game_list()