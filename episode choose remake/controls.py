ALLOWED_CONTROLS = {"-", "--", "q", "r", ""}

def print_controls():
    print("[-] Финальная сессия")
    print("[--] Откат")
    print("[Q] Добавить игру в очередь")
    print("[R] Рестарт")

def get_controls():
    control = "asdadasds"
    while control not in ALLOWED_CONTROLS:
        print_controls()
        control = input()
        control = control.lower()
    return control