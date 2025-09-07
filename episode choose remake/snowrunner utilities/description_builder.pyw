from collections import OrderedDict
import json
import os
from subprocess import run
from pyperclip import copy
os.chdir(os.path.dirname(os.path.abspath(__file__)))



if __name__ == "__main__":
    region = "Залив Педро"
    with open("names.txt", "r", encoding="utf-8") as f:
        names = f.read().splitlines()
    with open("contracts.json", "r", encoding="utf-8") as f:
        contracts = json.load(f)

    result = OrderedDict()

    for name in names:
        company = contracts.get(name, region)
        if company not in result:
            result[company] = []
        result[company].append(name)

    # Формируем итоговую строку
    output = ""
    for company, contracts_list in result.items():
        output += f"○ {company}\n"
        for contract in contracts_list:
            output += f"• {contract}\n"
        output += "\n"

    output = output.strip()  # убираем лишний перенос в конце

    copy(output)
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write(output)
    
    subl = r"D:\Program Files\Sublime Text\sublime_text.exe"
    run([subl, "description.txt"])