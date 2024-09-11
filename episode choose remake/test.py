import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw

def create_text(parent, text, font_path, font_size):
    # Создаем изображение с текстом
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGBA', (200, 50), (21, 21, 21, 255))  # Черный фон
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=font, fill="white")
    
    # Конвертируем изображение в PhotoImage
    return ImageTk.PhotoImage(image)

def create_top(parent, font_path, font_size, bgcolor):
    img_path = "gitignore/icons/SnowRunner.png"
    
    # Создаем фрейм
    frame = tk.Frame(parent, bg=bgcolor)
    frame.pack()
    
    # Загрузка и изменение размера изображения
    image = Image.open(img_path)
    image = image.resize((50, 50))
    photo = ImageTk.PhotoImage(image)
    
    # Создаем и размещаем виджет с изображением
    img_label = tk.Label(frame, image=photo, bg=bgcolor)
    img_label.photo = photo
    img_label.pack(side=tk.LEFT)
    
    # Создаем и размещаем текстовый виджет
    text_image = create_text(frame, "ДДД", font_path, font_size)
    text_label = tk.Label(frame, image=text_image, bg=bgcolor)
    text_label.image = text_image
    text_label.pack(side=tk.LEFT, padx=10)

# Пример использования:
def main():
    root = tk.Tk()
    
    # Установите заголовок окна
    root.title("My Application")
    
    # Установите размеры окна и разместите его по центру
    window_width = 400
    window_height = 300
    center_window(root, window_width, window_height)
    
    # Установите цвет фона
    bgcolor = "#151515"
    
    # Путь к кастомному шрифту и размер шрифта
    font_path = "path_to_your_custom_font.ttf"
    font_size = 24
    
    # Создайте top
    create_top(root, font_path, font_size, bgcolor)
    
    root.mainloop()

def center_window(window, width, height):
    # Получаем размеры экрана
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Рассчитываем позицию окна для центрации
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Устанавливаем размер и позицию окна
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    main()
