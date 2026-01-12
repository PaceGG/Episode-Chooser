import ctypes
import os

def set_window_pos(icon_path, title, x, y, width, height):
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    hwnd = kernel32.GetConsoleWindow()

    # Позиция и размеры
    user32.MoveWindow(hwnd, x, y, width, height, True)

    # Заголовок
    user32.SetWindowTextW(hwnd, title)

    # Загружаем иконку из файла
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    hicon = user32.LoadImageW(
        0,
        icon_path,
        IMAGE_ICON,
        256,
        256,
        LR_LOADFROMFILE
    )

    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1

    # Для заголовка
    user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hicon)
    # Для панели задач
    user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)




set_window_pos(r"..\Visual Elements\icon-square.ico", "Episode Chooser", 472, 276, 374, 444)
os.system('mode con: cols=50 lines=28')