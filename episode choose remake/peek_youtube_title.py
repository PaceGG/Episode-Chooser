from data import Data
from os import system
system("cls")
titles = Data("titles").titles
print(*titles, sep="\n") if len(titles) > 0 else print("Нет видео")
while True:
    pass