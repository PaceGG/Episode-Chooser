import dearpygui.dearpygui as dpg
from pages.main_page import create_main_page
from pages.settings_page import create_settings_page

dpg.create_context()

# ------------------------- Функции -------------------------
def show_main():
    dpg.show_item("main_page")
    dpg.hide_item("settings_page")

def show_settings():
    dpg.hide_item("main_page")
    dpg.show_item("settings_page")

def run_console_command():
    user_input = dpg.get_value("input_text")
    output = f"Вы ввели: {user_input}"
    dpg.set_value("output_text", output)
    dpg.set_value("log_text", dpg.get_value("log_text") + f"> {user_input}\n")

# ------------------------- Шрифт -------------------------
with dpg.font_registry():
    with dpg.font("C:/Windows/Fonts/arial.ttf", 16) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font(default_font)

# ------------------------- Создание окна -------------------------
with dpg.window(label="Моё приложение", width=600, height=400, no_resize=True):
    create_main_page(run_console_command, show_settings)
    create_settings_page(show_main)

# ------------------------- Запуск -------------------------
dpg.create_viewport(title='Моё приложение', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
