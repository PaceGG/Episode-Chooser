from data import Data
import youtube_utils as yt


class DataCollection:
    stat: Data
    empty_messages: list[yt.EmptyMessage]
    titles: list[yt.Title]

    def __init__(self):
        print("Инициализация данных")
        self.stat = Data("stat")
        self.empty_messages = Data("empty_messages").empty_messages
        self.titles = Data("titles").titles

    def edit_empty_messages(self):
        yt.edit_empty_messages(self.empty_messages, self.stat)