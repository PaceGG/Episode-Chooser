import tkinter as tk
from PIL import Image, ImageTk

def show_image(image_path, width=None, height=None, width_percent_of_screen=None, height_percent_of_screen=None, duration=3000):
    root = tk.Tk()
    root.title("Image Display")
    
    root.overrideredirect(True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Загружаем изображение
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Файл не найден: {image_path}")
        return

    aspect_ratio = image.width / image.height

    if width and height:
        image = image.resize((width, height), Image.LANCZOS)
    elif width:
        image = image.resize((width, int(width/aspect_ratio)), Image.LANCZOS)
    elif height:
        image = image.resize((int(height*aspect_ratio), height), Image.LANCZOS)

    if width_percent_of_screen and height_percent_of_screen:
        image = image.resize((int(screen_width * width_percent_of_screen), int(screen_height * height_percent_of_screen)), Image.LANCZOS)
    elif width_percent_of_screen:
        image = image.resize((int(screen_width * width_percent_of_screen), int(screen_width * width_percent_of_screen / aspect_ratio)), Image.LANCZOS)
    elif height_percent_of_screen:
        image = image.resize((int(screen_height * height_percent_of_screen * aspect_ratio), int(screen_height * height_percent_of_screen)), Image.LANCZOS)

    photo = ImageTk.PhotoImage(image)

    image_label = tk.Label(root, image=photo)
    image_label.pack()

    window_width = image.width
    window_height = image.height
    position_top = (screen_height - window_height) // 2
    position_left = (screen_width - window_width) // 2
    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    root.after(0)
    
    root.after(duration, root.destroy)

    root.mainloop()