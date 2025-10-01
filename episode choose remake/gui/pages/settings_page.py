import dearpygui.dearpygui as dpg

def create_settings_page(show_main_callback):
    with dpg.group(tag="settings_page", show=False):
        dpg.add_text("Страница настроек")
        dpg.add_checkbox(label="Включить что-то")
        dpg.add_slider_float(label="Настройка уровня", default_value=0.5, max_value=1.0)
        dpg.add_button(label="Назад на главную", callback=show_main_callback)
