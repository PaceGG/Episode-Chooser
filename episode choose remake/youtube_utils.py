import os
from dotenv import load_dotenv
from util import intc
from time_format import today, get_time
load_dotenv("gitignore/.env")


class EmptyMessage:
    name: str
    ep_range: list[int]
    message_id: int

    def __init__(self, name, ep_range, message_id):
        self.name = name
        self.ep_range = ep_range
        self.message_id = message_id

    def __repr__(self):
        return f"emptyMessage({self.name} {self.ep_range} {self.message_id})"
    

class Title:
    name: str
    episode: int
    is_final: bool

    def __init__(self, name, episode, is_final=False):
        self.name = name
        self.episode = episode  
        self.is_final = is_final

    def __repr__(self):
        if self.episode == -1:
            self.episode = -2
            return f"{get_time()}"
        elif self.episode == 0:
            self.episode = -1
            return f"{self.name}"
        elif self.episode == 1:
            self.episode = 0
            return f"• № 1 • {self.name}"
        else:
            episode = self.episode
            self.episode = -1
            return f"• № {episode}{f" - Финал" if self.is_final else ""} • {self.name}"


def add_titles(titles: list[Title], game, count_videos):
    for episode_num in range(game.count_episode + 1, game.count_episode + count_videos + 1):
        titles.append(Title(game.full_name, episode_num))

def add_empty_message(empty_messages: list[EmptyMessage], game, count_videos, message_id):
    empty_messages.append(EmptyMessage(game.name, [game.count_episode + 1, game.count_episode + count_videos], message_id))

def get_yt_videos():
    from googleapiclient.discovery import build

    api_key = os.getenv("YT_API_KEY")
    channel_id = "UC2Y71nJHtoLzY88Wrrqm7Kw"

    youtube = build("youtube", 'v3', developerKey=api_key)

    channels_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=25
    )

    try:
        playlist_response = playlist_request.execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    videos = {}

    for item in playlist_response['items']:
        try: name, number, game = item['snippet']['title'].split(" • ")
        except: continue

        number = intc(number)

        try: videos[game][number] = name
        except: videos[game] = {number: name}

    return videos

def edit_empty_message(empty_message: EmptyMessage, yt_videos):
    import telegram_utils

    if empty_message.name not in yt_videos: return False
    videos = yt_videos[empty_message.name]

    names = []
    for episode_number in range(empty_message.ep_range[0], empty_message.ep_range[1] + 1):
        episode_number = str(episode_number)
        if episode_number in videos.keys():
            names.append(videos[episode_number])

    if len(names) != empty_message.ep_range[1] - empty_message.ep_range[0] + 1: return False

    titles = ""
    for name in names:
        titles += f"• {name}\n"

    if names:
        new_text = f"{empty_message.name}: № {empty_message.ep_range[0]}{f"-{empty_message.ep_range[0] + len(names)-1}" if len(names) > 1 else ""}:\n{titles}"
        telegram_utils.edit_caption(new_text, empty_message.message_id)

        return True
    
    return False

def edit_empty_messages(empty_messages, stat):
    if today() - stat.last_update < 12*60*60 and __name__ != "__main__": return

    yt_videos = get_yt_videos()
    for empty_message in empty_messages:
        edit_empty_message(empty_message, yt_videos)

    stat.last_update = today()