from collections import OrderedDict
import json
import os
from subprocess import run
from pyperclip import copy
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def convert_names(names, region=None):
    if region == None:
        with open("region_name.txt", "r", encoding="utf-8") as f:
            region = f.read().strip()
    with open("contracts.json", "r", encoding="utf-8") as f:
        contracts = json.load(f)

    lines = []
    prev_company = None

    for name in names:
        company = contracts.get(name, region)
        if company != prev_company:
            if lines:
                lines.append("") 
            lines.append(f"○ {company}")
            prev_company = company
        lines.append(f"• {name}")

    return lines

if __name__ == "__main__":
    with open("3-names.txt", "r", encoding="utf-8") as f:
        names = f.read().splitlines()

    lines = convert_names(names)

    output = "\n".join(lines).strip()

    copy(output)

    description_file_name = "4-description.txt"

    with open(description_file_name, "w", encoding="utf-8") as f:
        f.write(output)
    
    subl = r"D:\Files\Sublime Text\sublime_text.exe"
    run([subl, description_file_name])