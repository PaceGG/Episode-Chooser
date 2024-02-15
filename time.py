from pyperclip import *

x = paste()

x_list = x.split(',')

data = []
for i in range(len(x_list)):
    number = ''
    for x in range(len(x_list[i])):
        if x_list[i][x].isdigit():
            number += x_list[i][x]
    data.append(int(number))

if len(data) == 4:
    data[1] += data[0]*24
    data.pop(0)
    
time = []
for i in data:
    i = str(i)
    if len(i) == 1:
        i = '0' + i
    time.append(i)

time_str = f'{time[0]}:{time[1]}:{time[2]}'

print(time_str)
copy(time_str)