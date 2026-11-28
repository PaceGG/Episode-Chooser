# ALLOWED_CONTROLS = {"-", "--", "q", "r", ""}

CONTROLS_LABELS = {
    "-": "Финальная сессия",
    "--": "Откат",
    "Q": "Добавить игру в очередь",
    "R": "Рестарт приложения",
    "W": "Запуск игры"
}

def print_controls(controls, labels: dict[str, str] | None = None):
    if labels is None: labels = CONTROLS_LABELS
    for control in controls:
        label = labels.get(control)
        if label is None: continue
        print(f"[{control}] {label}")

def get_controls(allowed_controls):
    while True:
        print_controls(allowed_controls)
        control = input().lower()
        if control in allowed_controls:
            return control
