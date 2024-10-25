from YTTitle import show_yt_title
import os

import PATHS
os.chdir(PATHS.repository)

if __name__ == "__main__":
    yt_titles = show_yt_title()
    print(*yt_titles, sep="\n")
    while True:
        pass