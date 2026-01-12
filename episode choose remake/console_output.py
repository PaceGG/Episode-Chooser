import re

def hex_to_rgb(hex_color) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_hex(text: str, hex_color: str) -> str:
    r, g, b = hex_to_rgb(hex_color)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def hr(text: str = '', width: int = 42, char: str = '=', color: str = '#ffffff') -> str:
    if visible_length(text) > width:
        return color_hex(text, color) + "\n"
    if text:
        text = f" {text} "
        remaining = width - visible_length(text)
        if remaining < 0:
            line = text[:width]
        else:
            left = remaining // 2
            right = remaining - left
            line = char * left + text + char * right
    else:
        line = char * width

    return color_hex(line, color) + "\n"

def get_strings_width(strings):
    return visible_length(max(strings.split("\n"), key=len))

def borders(text: str, border_text:str = '', color = "#ffffff"):
    width = get_strings_width(text)
    text = hr(border_text, color=color, width=width) + text
    text += hr(color=color, width=width)

    return text

def get_chance_color(games):
    """
        Возвращает цвет более вероятной игры или белый, если шансы равны
    """
    return "#ffffff" if games[0].chance == games[1].chance == 1 else max(games, key=lambda g: g.chance).color

def get_time__limit_color(games):
    return min(games, key=lambda g: g.time_limit).color

def visible_length(text: str) -> int:
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    return len(ansi_escape.sub('', text))