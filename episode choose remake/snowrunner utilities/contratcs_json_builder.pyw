import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Путь к текстовому файлу
file_path = "contracts.txt"

contracts_dict = {}
current_company = None

with open(file_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            # Пустая строка – пропускаем
            continue
        if current_company is None:
            # Первая строка блока – название компании
            current_company = line
        else:
            # Строки после компании – контракты
            contracts_dict[line] = current_company
            # Проверяем, не начался ли новый блок (по логике: новая компания идет после пустой строки)
            # В нашем случае пустые строки уже пропущены, поэтому новый блок определяется автоматически на следующей итерации
            # Если следующая строка – это новая компания, она будет определена как current_company
            # Для этого нам нужен флаг конца блока. Проще – менять current_company при обнаружении строки без запятой или точки? 
            # Но в нашем формате проще:
            # После серии контрактов идет пустая строка, которая обнуляет current_company
        if line == current_company:
            # Если случайно повторение названия компании как контракта, пропускаем
            continue
    # Чтобы корректно определить новую компанию, можно использовать такой подход:
    # Но проще – раз блоки отделены пустыми строками, достаточно делать:
    # если пустая строка, current_company = None
        # Точно:
        # current_company останется None после пустой строки
    if line == "":
        current_company = None

# Альтернатива с правильной обработкой блоков:
contracts_dict = {}
current_company = None
with open(file_path, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            current_company = None  # конец блока
            continue
        if current_company is None:
            current_company = line  # название компании
        else:
            contracts_dict[line] = current_company

# Сохраняем в JSON
with open("contracts.json", "w", encoding="utf-8") as f:
    json.dump(contracts_dict, f, ensure_ascii=False, indent=2)

print("JSON создан: contracts.json")
