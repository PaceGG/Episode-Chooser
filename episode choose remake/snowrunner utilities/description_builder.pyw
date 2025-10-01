from collections import OrderedDict
import json
import os
from subprocess import run
from pyperclip import copy
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    region = "Болота"
    with open("names.txt", "r", encoding="utf-8") as f:
        names = f.read().splitlines()
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

    output = "\n".join(lines).strip()

    copy(output)
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write(output)
    
    subl = r"D:\Program Files\Sublime Text\sublime_text.exe"
    run([subl, "description.txt"])