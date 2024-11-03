from YTTitle import yt_title_pop
from pyautogui import hotkey
from pyperclip import copy
from timeFormat import get_time
import os
from time import sleep
from setEngLayout import set_eng_layout

import PATHS
os.chdir(PATHS.repository)

if __name__ == "__main__":
    set_eng_layout()
    unicode_string = yt_title_pop()
    copy(unicode_string)
    # sleep(1)
    hotkey('ctrl', 'v')
