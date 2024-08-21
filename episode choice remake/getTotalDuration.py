from moviepy.video.io.VideoFileClip import *

directory = r"D:\Program Files\Shadow Play\SnowRunner"

if __name__ == "__main__":
    total_duration_seconds = get_total_duration(directory)
    print(total_duration_seconds)
    total_duration_minutes = total_duration_seconds // 60
    print(f"Суммарная продолжительность: {total_duration_minutes} минут")
