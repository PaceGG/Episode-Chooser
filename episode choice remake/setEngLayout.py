import win32api
import win32gui

def set_eng_layout():
    window_handle = win32gui.GetForegroundWindow()
    result = win32api.SendMessage(window_handle, 0x0050, 0, 0x04090409)
    return(result)

if __name__ == "__main__":
    set_eng_layout()