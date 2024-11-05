import os
import shutil

def move_files(source_folder, destination_folder):
    """
    Перемещает все файлы из исходной папки в целевую папку.
    
    :param source_folder: Путь к исходной папке
    :param destination_folder: Путь к целевой папке
    """
    # Проверка, существует ли исходная папка
    if not os.path.exists(source_folder):
        print(f"Исходная папка '{source_folder}' не найдена.")
        return

    # Проверка, существует ли целевая папка, если нет - создаем ее
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Перемещение файлов
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)

        # Проверка, что это файл, а не папка
        if os.path.isfile(source_file):
            shutil.move(source_file, destination_file)
            print(f"Перемещен: {filename}")

# Пример использования:
# move_files('path/to/source_folder', 'path/to/destination_folder')
