import dearpygui.dearpygui as dpg

def create_main_page(run_command_callback, show_settings_callback):
    with dpg.group(tag="main_page"):
        dpg.add_text("Главная страница")
        dpg.add_input_text(tag="input_text", label="Введите команду")
        dpg.add_button(label="Запустить команду", callback=run_command_callback)
        dpg.add_separator()
        dpg.add_text("Вывод:")
        dpg.add_text("", tag="output_text")
        dpg.add_separator()
        dpg.add_button(label="Настройки", callback=show_settings_callback)
        dpg.add_separator()
        dpg.add_text("Лог команд:")
        dpg.add_input_text(tag="log_text", multiline=True, readonly=True, height=100)
