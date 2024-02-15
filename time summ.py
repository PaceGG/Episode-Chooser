from pyperclip import *

times = paste()

# times = '''Mafia: Definitive Edition - 10/21 (17:35:23)
# Mafia II: Definitive Edition - 11/23 (23:56:27)
# Mafia III: Definitive Edition - 34/35 (20:20:20)'''

# Time calculate

times_list = times.split('\n')

while '' in times_list:
    times_list.remove('')
    
for i in range(len(times_list)):
    first_bracket = times_list[i].index('(')
    second_bracket = times_list[i].index(')')

    times_list[i]=times_list[i][first_bracket+1:second_bracket]
    
global_hours = 0
global_minutes = 0
global_secs = 0

for i in times_list:
    hours,minutes,secs = i.split(':')
    global_hours += int(hours)
    global_minutes += int(minutes)
    global_secs += int(secs)

if global_secs >= 60:
    global_minutes += global_secs // 60
    global_secs %= 60
if global_minutes >= 60:
    global_hours += global_minutes // 60
    global_minutes %= 60
if len(str(global_hours)) == 1:
    global_hours = f'0{global_hours}'

if len(str(global_minutes)) == 1:
    global_minutes = f'0{global_minutes}'
    
if len(str(global_secs)) == 1:
    global_secs = f'0{global_secs}'
    
# print(global_hours,global_minutes,global_secs,sep=':')

# episodes calculate

eps_list = times.split('\n')

while '' in eps_list:
    eps_list.remove('')
    
for i in range(len(eps_list)):
    first_bracket = eps_list[i].rfind('- ')
    second_bracket = eps_list[i].find('(')

    eps_list[i]=eps_list[i][first_bracket+2:second_bracket]
    
true_eps = 0
all_eps = 0

for ep in eps_list:
    if '/' in ep:
        true_eps += int(ep[:ep.find('/')])
        all_eps += int(ep[ep.find('/')+1:])
    else:
        true_eps += int(ep)
        all_eps += int(ep)
        
add_info = f' - {true_eps}/{all_eps} ({global_hours}:{global_minutes}:{global_secs})'

print(add_info)
copy(add_info)