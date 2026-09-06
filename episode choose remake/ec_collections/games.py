from game import Game
import paths

class GamesCollection:
    games: list[Game]

    def __init__(self):
        print("Инициализация игр")
        self.games = [Game(name=game_name) for game_name in paths.game_names[:2]]
        self.games.append(Game(name="SnowRunner [ng+]", safe_name="SnowRunner"))

    def __repr__(self):
        return self.games