import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_region(image_path: str, region: tuple[int, int, int, int]) -> str:
    """
    Извлекает текст с изображения в указанной области и сохраняет обрезанную область.
    :param image_path: путь к изображению
    :param region: координаты области (left, upper, right, lower)
    :param save_dir: папка для сохранения cropped-изображения (если None – сохраняется рядом с исходным)
    :return: текст в указанной области
    """
    image = Image.open(image_path)
    cropped_image = image.crop(region)
    text = pytesseract.image_to_string(cropped_image, lang="rus")
    return text.strip()

def get_name(image_path: str) -> str:
    """
    Извлекает имя игры из изображения.
    :param image_path: путь к изображению
    :return: имя игры
    """
    region = (1263, 298, 1637, 343)
    name = extract_text_from_region(image_path, region)
    if not name:
        error_text = str(image_path).split('\\')[-1]
        error_text = error_text.split(" ")[-1]
        return f"Error: {error_text}"
    return name

def get_names(folder_path: str) -> list[str]:
    names = []
    folder_path: Path = Path(folder_path)
    for image_path in folder_path.iterdir():
        if not image_path.suffix == ".png": continue
        name = get_name(image_path)
        names.append(name)
    return names

if __name__ == "__main__":
    names = get_names(r"D:\Program Files\Videos\SnowRunner")
    with open("names.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(names))