import time
import math
import random
import dearpygui.dearpygui as dpg

# ---------------------------- Конфигурация ---------------------------------
ITEM_W = 180
ITEM_H = 140
VISIBLE_COUNT = 7
DRAW_W = ITEM_W * VISIBLE_COUNT
DRAW_H = ITEM_H + 40
CENTER_X = DRAW_W // 2

# Предопределённый победитель: индекс в списке skins
winner_index = 2
skins = [
    ("AK-47 | Redline", "Industrial"),
    ("M4A1-S | Hyper Beast", "Covert"),
    ("AWP | Asiimov", "Restricted"),
    ("Glock-18 | Fade", "Mil-Spec"),
    ("Desert Eagle | Blaze", "Covert"),
    ("USP-S | Kill Confirmed", "Classified"),
    ("CZ75-Auto | Victoria", "Mil-Spec"),
    ("P90 | Emerald Dragon", "Restricted"),
    ("Nova | Rust Coat", "Consumer"),
]

# ---------------------------------------------------------------------------
animating = False
anim_start_time = 0.0
anim_duration = 4.5
anim_start_offset = 0.0
anim_total_distance = 0.0
current_offset = 0.0
draw_ids = []
RARITY_COLORS = {
    "Consumer": (150, 150, 150, 255),
    "Industrial": (70, 120, 180, 255),
    "Mil-Spec": (60, 180, 75, 255),
    "Restricted": (200, 180, 30, 255),
    "Classified": (180, 80, 200, 255),
    "Covert": (220, 60, 60, 255),
}

# ---------------------------- Easing ---------------------------------------
def ease_out_cubic(t: float) -> float:
    return 1 - pow(1 - t, 3)

# ---------------------------- Рисование ------------------------------------
def clear_drawlist():
    global draw_ids
    for _id in draw_ids:
        try:
            dpg.delete_item(_id)
        except Exception:
            pass
    draw_ids = []


def draw_skins(offset_px: float):
    clear_drawlist()
    parent = "roulette_drawlist"
    total = len(skins)
    total_width = total * ITEM_W

    # offset_px может быть любым положительным числом — индексы рассчитываются с циклической обёрткой
    start_idx_float = offset_px / ITEM_W
    first_index = int(math.floor(start_idx_float)) - 1
    count_to_draw = VISIBLE_COUNT + 6

    for i in range(count_to_draw):
        idx = (first_index + i) % total
        element_x = (first_index + i) * ITEM_W - offset_px
        draw_x = int(element_x + DRAW_W // 2)
        x0 = draw_x - ITEM_W // 2
        y0 = 16
        x1 = x0 + ITEM_W - 8
        y1 = y0 + ITEM_H
        name, rarity = skins[idx]
        color = RARITY_COLORS.get(rarity, (120, 120, 120, 255))
        rect_id = dpg.draw_rectangle((x0, y0), (x1, y1),
                                     color=color,
                                     fill=(color[0], color[1], color[2], 40),
                                     thickness=2,
                                     parent=parent)
        draw_ids.append(rect_id)
        txt_id = dpg.draw_text((x0 + 8, y0 + 8), name, size=14, parent=parent)
        draw_ids.append(txt_id)
        rarity_id = dpg.draw_text((x0 + 8, y1 - 22), rarity, size=12, parent=parent)
        draw_ids.append(rarity_id)

    # маркер-рамка по центру
    cx0 = DRAW_W // 2 - ITEM_W // 2
    cy0 = 8
    cx1 = cx0 + ITEM_W - 8
    cy1 = cy0 + ITEM_H + 8
    marker_id = dpg.draw_rectangle((cx0, cy0), (cx1, cy1),
                                   color=(255, 220, 0, 255),
                                   thickness=3,
                                   parent=parent)
    draw_ids.append(marker_id)

# ---------------------------- Анимация -------------------------------------
def start_spin_callback():
    global animating, anim_start_time, anim_start_offset, anim_total_distance, anim_duration
    global current_offset, winner_index

    if animating:
        return

    animating = True
    anim_start_time = time.time()
    anim_start_offset = current_offset

    total = len(skins)
    total_width = total * ITEM_W
    winner_pos = winner_index * ITEM_W + ITEM_W // 2

    # текущая позиция в пределах полного цикла
    cur_mod = anim_start_offset % total_width

    # сколько циклов прокруток (визуально) — случайно
    cycles = random.randint(3, 6)

    # расстояние от текущего модуля до позиции победителя
    delta_to_winner = (winner_pos - cur_mod + total_width) % total_width

    # итоговое перемещение (в пикселях). При завершении мы выставим current_offset = anim_start_offset + anim_total_distance
    anim_total_distance = cycles * total_width + delta_to_winner

    base_duration = 3.2
    extra_per_cycle = 0.6
    anim_duration = base_duration + cycles * extra_per_cycle

    dpg.configure_item("status_text", default_value="Крутим...")

    # регистрируем колбэк на следующий кадр
    dpg.set_frame_callback(dpg.get_frame_count() + 1, animate_frame)


def animate_frame(sender=None, app_data=None):
    """Колбэк кадра. Если анимация ещё не окончена — перерисовывает и регистрирует себя на следующий кадр."""
    global animating, anim_start_time, anim_start_offset, anim_total_distance, anim_duration
    global current_offset, draw_ids, winner_index

    if not animating:
        return

    now = time.time()
    t = (now - anim_start_time) / anim_duration
    finished = False
    if t >= 1.0:
        t = 1.0
        finished = True

    eased = ease_out_cubic(t)
    current_offset = anim_start_offset + anim_total_distance * eased

    draw_skins(current_offset)

    if finished:
        animating = False

        # ВАЖНО: выставляем точную окончательную абсолютную позицию без лишней нормализации через modulo.
        # Это позволяет избежать визуального «перескакивания» назад по модулю и удерживает рулетку на месте.
        final_offset = anim_start_offset + anim_total_distance
        current_offset = final_offset
        draw_skins(current_offset)

        name, rarity = skins[winner_index]
        dpg.configure_item("status_text", default_value=f"Вы выиграли: {name} ({rarity})")

        with dpg.window(label="Победа!", modal=True, show=True, width=360, height=160) as win_id:
            dpg.add_text(f"Вы выиграли:\n{name}\n{rarity}")
            dpg.add_separator()
            dpg.add_button(label="OK", width=100, callback=lambda s, a: dpg.delete_item(win_id))

        # анимация завершена — больше колбэков не регистрируем
    else:
        # регистрируем себя на следующий кадр
        dpg.set_frame_callback(dpg.get_frame_count() + 1, animate_frame)

# ---------------------------- UI -------------------------------------------
def create_ui():
    dpg.create_context()
    dpg.create_viewport(title='CS:GO стиль — Рулетка (DearPyGui)', width=900, height=400)
    main_win_tag = "main_window"

    with dpg.window(label="Рулетка", width=880, height=360, pos=(10, 10), tag=main_win_tag):
        dpg.add_text("Рулетка стиля CS:GO — демо с заглушками")
        dpg.add_spacer()
        with dpg.group(horizontal=True):
            dpg.add_button(label="Spin", callback=lambda s, a: start_spin_callback(), width=120)
            dpg.add_spacer()
            dpg.add_text("Status:", indent=10)
            dpg.add_text("Ready", tag="status_text")
        dpg.add_spacer()
        dpg.add_separator()
        with dpg.drawlist(width=DRAW_W, height=DRAW_H, tag="roulette_drawlist"):
            pass
        dpg.add_spacer()
        dpg.add_text("Предопределённый победитель: ", bullet=True)
        dpg.add_text(f"Index = {winner_index} — {skins[winner_index][0]} ({skins[winner_index][1]})")

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # начальная отрисовка
    draw_skins(current_offset)

    if dpg.does_item_exist(main_win_tag):
        dpg.set_primary_window(main_win_tag, True)
    else:
        print(f"[WARN] Primary window tag '{main_win_tag}' not found — skipping set_primary_window()")

    dpg.start_dearpygui()
    dpg.destroy_context()

# --------------------------------- Run -------------------------------------
if __name__ == '__main__':
    create_ui()
