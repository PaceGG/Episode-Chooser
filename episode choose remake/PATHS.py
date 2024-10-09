import os

game = [
    r"D:\Games\Far Cry 3\bin\farcry3.lnk",
    r"D:\Games\Wolfenstein\Wolfenstein.lnk",
    'C:\\ProgramData\\TileIconify\\SnowRunner\\SnowRunner.vbs'
]

extra_names = [
    "", # First game
    "", # Second game
    "Мичиган", # Extra/third game
]

video = "D:/Program Files/Shadow Play"

repository = os.path.dirname(os.path.dirname(__file__)) # automacy