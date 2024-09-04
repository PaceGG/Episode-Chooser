from YTTitle import yt_title_pop
from pyautogui import hotkey
from pyperclip import copy
from timeFormat import get_time
import os

os.chdir("D:\\Program Files\\HTML\\Games")

if __name__ == "__main__":
    unicode_string = yt_title_pop()
    copy(unicode_string)
    hotkey('ctrl', 'v')
    copy(get_time())
