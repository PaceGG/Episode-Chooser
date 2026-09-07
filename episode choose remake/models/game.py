from dataclasses import dataclass

@dataclass
class Game:
    name: str
    safe_name: str
    short_name: str
    extra_name: str
    full_name: str
    color: str

    game_path: str
    video_dir: str

    count_session: int = 0
    count_episode: int = 0
    time_limit: int = 120
    content_time: int = 0
    user_time: int = 0

    chance: int = 1
    is_selected: bool

    header: str

    def content_time_format(self):
        content_time_debt = -self.content_time
        sign = "+" if content_time_debt > 0 else ""
        return f"{sign}{content_time_debt}"

    def __repr__(self):
            return f"class {self.__class__.__name__}(\n{'\n'.join(f'{k} = {v!r}' for k, v in vars(self).items())})"

    def to_dict(self):
        return {
            "name": self.name,
            "count_session": self.count_session,
            "count_episode": self.count_episode,
            "time_limit": self.time_limit,
            "content_time": self.content_time,
            "user_time": self.user_time
        }