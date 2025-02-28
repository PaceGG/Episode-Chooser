print("Загрузка модуля roulette")
import random
import time
import os
from colorama import init
init()

def hex_to_rgb(hex_color) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def print_colored_hex(text: str, hex_color: str):
    r, g, b = hex_to_rgb(hex_color)
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_screen(step, blink=False, color=None):
    global roulette
    screen = roulette[step:step+SCREEN_SIZE]
    clear_console()
    for i in range(SCREEN_SIZE):
        prefix = "> " if i == SCREEN_SIZE // 2 else "      "
        element = screen[i].name if not blink or i != SCREEN_SIZE // 2 else " "
        custom_color = screen[i].color if color is None or i == SCREEN_SIZE // 2 else color
        print_colored_hex(prefix + element, hex_color=custom_color)


def blink_screen(step):
    global roulette
    screen = roulette[step:step+SCREEN_SIZE]
    for frame in range(2*5):
        clear_console()
        print_screen(step, blink=(frame % 2 == 0), color="#111111")
        time.sleep(0.5)
    

def spin_wheel(pattern):
    start_step = 0
    for step in range(start_step, start_step + pattern[0] - SCREEN_SIZE//2):
        print_screen(step)
        progress = step / pattern[0]
        sleep_time = initial_sleep_time + (max_sleep_time - initial_sleep_time) * (progress ** 2)
        time.sleep(sleep_time)

    start_step += pattern[0] - SCREEN_SIZE//2
    for step in range(start_step, start_step + pattern[1]):
        print_screen(step)
        sleep_time = 0.5
        time.sleep(sleep_time)

    start_step += pattern[1]
    for step in range(start_step, start_step + pattern[2]):
        print_screen(step)
        if step == start_step + pattern[2] - 1 and roulette[step:step+SCREEN_SIZE][SCREEN_SIZE//2] != roulette[step+1:step+1+SCREEN_SIZE][SCREEN_SIZE//2]:
            print("Final chance!")
            time.sleep(5)
        else: 
            time.sleep(1)

    start_step += pattern[2]
    for step in range(start_step, start_step + pattern[3]):
        print_screen(step)

    blink_screen(step)

def spin_roulette(games, skip=False, winner=None):
    winner = choose_winner(games) if not winner else winner
    if skip: return winner

    global SCREEN_SIZE, initial_sleep_time, max_sleep_time, roulette
    total_lines = 10
    SCREEN_SIZE = total_lines + (total_lines % 2 == 0)

    pattern = [random.randint(30,50), random.randint(5,10), random.randint(3,5), random.randint(0,1)]

    roulette = [choose_winner(games) for _ in range(50+10+5+1+SCREEN_SIZE//2)]
    winner_game = sum(pattern) - 1
    roulette[winner_game] = winner
    


    initial_sleep_time = 0.05
    max_sleep_time = 0.5

    spin_wheel(pattern)

    return winner

def choose_winner(games):
    return random.choices(games, weights=[game.chance for game in games])[0]