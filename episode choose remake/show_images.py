# image_selector_interactive.py
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

def select_image_from_urls(url_list, window_title="Выбор изображения", window_position=(942, 193), window_size=(528, 631)) -> str:
    """
    Загружает изображения по URL, показывает рабочие изображения в столбик с индексами слева.
    Пользователь выбирает изображение кликом на изображение.
    Возвращает выбранный URL.
    """
    working_images = []
    working_urls = []
    broken_urls = []

    # Загружаем изображения
    for url in url_list:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            working_images.append(img)
            working_urls.append(url)
        except Exception:
            broken_urls.append(url)

    if not working_images:
        print("Нет доступных изображений.")
        return None

    n = len(working_images)

    if n == 1:
        return working_urls[0]
    
    fig, axes = plt.subplots(n, 1, figsize=(6, 4 * n))
    if n == 1:
        axes = [axes]

    for idx, (ax, img) in enumerate(zip(axes, working_images), start=1):
        ax.imshow(img)
        ax.axis("off")

    plt.tight_layout()

    # Настройка окна: размер, позиция, заголовок
    manager = plt.get_current_fig_manager()
    try:
        manager.window.wm_title(window_title)
        manager.window.wm_geometry(f"{window_size[0]}x{window_size[1]}+{window_position[0]}+{window_position[1]}")
    except AttributeError:
        try:
            manager.window.setWindowTitle(window_title)
            manager.window.setGeometry(window_position[0], window_position[1], window_size[0], window_size[1])
        except Exception:
            print("Не удалось установить позицию/размер/заголовок окна")

    # Переменная для хранения выбранного URL
    selected_url = {"url": None}

    # Callback функция на клик
    def on_click(event):
        for idx, ax in enumerate(axes):
            if ax == event.inaxes:
                selected_url["url"] = working_urls[idx]
                plt.close(fig)  # закрываем окно сразу после выбора
                break

    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

    return selected_url["url"]
