print("Загрузка модуля youtube_utils")

import os
import json
import time
from dotenv import load_dotenv
from util import intc
from time_format import today, get_time

load_dotenv("gitignore/.env")


class EmptyMessage:
    name: str
    ep_range: list[int]
    durations: list[int]
    message_id: int
    timestamp: int

    def __init__(self, name, ep_range, durations, message_id, timestamp=None):
        self.name = name
        self.ep_range = ep_range
        self.durations = durations
        self.message_id = message_id
        self.timestamp = int(time.time()) if timestamp is None else timestamp

    def __repr__(self):
        return f"emptyMessage({self.name} {self.ep_range} {self.durations} {self.message_id})"


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
            return f"• № {episode}{f' - Финал' if self.is_final else ''} • {self.name}"


def add_titles(titles: list[Title], game, count_videos, is_final):
    for episode_num in range(game.count_episode + 1, game.count_episode + count_videos + 1):
        titles.append(
            Title(
                game.full_name,
                episode_num,
                is_final=is_final and episode_num == game.count_episode + count_videos
            )
        )


def add_empty_message(empty_messages: list[EmptyMessage], game, count_videos, durations, message_id):
    empty_messages.append(
        EmptyMessage(
            game.full_name,
            [game.count_episode + 1, game.count_episode + count_videos],
            durations,
            message_id
        )
    )


def get_yt_videos():
    print("Загрузка видео с Youtube")
    from googleapiclient.discovery import build

    api_key = os.getenv("YT_API_KEY")
    channel_id = "UC2Y71nJHtoLzY88Wrrqm7Kw"

    youtube = build("youtube", "v3", developerKey=api_key)

    # Получаем плейлист загруженных видео
    channels_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    try:
        playlist_response = playlist_request.execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

    videos = {}
    for item in playlist_response.get("items", []):
        snippet = item["snippet"]
        title_full = snippet["title"]
        video_id = snippet["resourceId"]["videoId"]
        description = snippet.get("description", "")
        publishedAt = snippet.get("publishedAt", "")

        try:
            name_part, number_part, game_part = title_full.split(" • ")
        except Exception:
            continue

        number = intc(number_part)

        if game_part not in videos:
            videos[game_part] = {}

        videos[game_part][str(number)] = {
            "title": name_part,
            "description": description,
            "publishedAt": publishedAt,
            "videoId": video_id
        }

    return videos


def add_sessions_entry_with_data(sessions_path: str, game: str, episodes: list[dict], message_id: int, timestamp: int):
    import json
    import os

    # читаем существующий файл
    try:
        with open(sessions_path, "r", encoding="utf-8") as f:
            sessions = json.load(f)
    except FileNotFoundError:
        sessions = {}
    except Exception:
        sessions = {}

    # используем message_id как ключ
    new_id = str(message_id)

    # создаём запись
    sessions[new_id] = {
        "game": game,
        "datetime": timestamp,  # берём дату сообщения
        "episodes": episodes
    }

    # атомарная запись
    tmp_path = sessions_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=4)
    os.replace(tmp_path, sessions_path)

    return new_id


def edit_empty_message(empty_message: EmptyMessage, yt_videos):
    import telegram_utils

    if empty_message.name not in yt_videos:
        return False

    videos = yt_videos[empty_message.name]
    episode_list = []
    names = []

    for episode_number in range(empty_message.ep_range[0], empty_message.ep_range[1] + 1):
        ep_str = str(episode_number)
        if ep_str in videos:
            ep_data = videos[ep_str]
            duration_index = episode_number - empty_message.ep_range[0]
            duration = empty_message.durations[duration_index]
            names.append(ep_data["title"])
            episode_list.append({
                "number": episode_number,
                "title": ep_data.get("title", ""),
                "description": ep_data.get("description", ""),
                "publishedAt": ep_data.get("publishedAt", ""),
                "videoId": ep_data.get("videoId", ""),
                "duration": duration,
            })

    if len(names) != empty_message.ep_range[1] - empty_message.ep_range[0] + 1:
        return False

    titles_text = "\n".join(f"• {name}" for name in names)
    new_text = f"{empty_message.name}: № {empty_message.ep_range[0]}{f'-{empty_message.ep_range[0] + len(names)-1}' if len(names) > 1 else ''}:\n{titles_text}"
    telegram_utils.edit_caption(new_text, empty_message.message_id)

    # --- добавляем запись в sessions.json ---
    sessions_path = r"D:\Program Files\HTML\Episode-Chooser\react-remake\public\sessions.json"
    try:
        add_sessions_entry_with_data(sessions_path, empty_message.name, episode_list, empty_message.message_id, empty_message.timestamp)
        print(f"Добавлена сессия для {empty_message.name} эпизоды {empty_message.ep_range[0]}-{empty_message.ep_range[1]}")
    except Exception as e:
        print(f"Не удалось добавить запись в sessions.json: {e}")



    return True


def edit_empty_messages(empty_messages, stat):
    if today() - stat.last_update < 12*60*60 and __name__ != "__main__":
        return

    yt_videos = get_yt_videos()

    empty_messages[:] = [
        empty_message for empty_message in empty_messages
        if not edit_empty_message(empty_message, yt_videos)
    ]

    stat.last_update = today()


if __name__ == "__main__":
    from data import Data

    videos = get_yt_videos()
    for game in videos.keys():
        print(f"{game}:")
        for number, info in videos[game].items():
            print(f"{number}: {info['title']} ({info['videoId']})")
        print()

    empty_messages: list[EmptyMessage] = Data("empty_messages").empty_messages
    stat = Data("stat")
    edit_empty_messages(empty_messages, stat)
