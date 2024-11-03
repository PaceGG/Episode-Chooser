import os
import json

repository = os.path.dirname(os.path.dirname(__file__)) # automacy

with open(os.path.join(repository, "react-remake/db.json"), encoding="utf-8") as f:
    data = json.load(f)["showcase"]

if __name__ == "__main__":
    print(data[0]["name"])
    print(data[1]["name"])

games_folder = "D:/Games"

#custom paths
game_0 = ""
game_1 = ""

game = [
    f"{os.path.join(games_folder, data[0]["name"].replace(':', ''), "game.lnk")}" if game_0 == "" else game_0,
    f"{os.path.join(games_folder, data[1]["name"].replace(':', ''), "game.lnk")}" if game_1 == "" else game_1,
    'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'
]

extra_names = [
    "", # First game
    "", # Second game
    "Мичиган", # Extra/third game
]

video = "D:/Program Files/Shadow Play"