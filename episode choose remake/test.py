import json
import PATHS

game_name = "Fallout: New Vegas"

with open("react-remake/db.json", encoding="utf-8") as f:
        showcase = json.load(f)["showcase"]

extra_name = ""
if game_name == "SnowRunner":
    extra_name = PATHS.extra_names[2]
else:
    for item in showcase:
        if item["name"] == game_name:
            extra_name = PATHS.extra_names[int(item["id"])]

if extra_name != "": game_name = f"{game_name}: {extra_name}"

print(game_name)