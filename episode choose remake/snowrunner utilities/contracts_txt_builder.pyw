import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import io

def extract_text_from_image_file(image_path):
    """
    Извлекает текст из изображения по указанному пути.

    :param image_path: Путь к изображению.
    :return: Извлеченный текст или None в случае ошибки.
    """
    try:
        # Открытие изображения
        image = Image.open(image_path)
        # Конвертация в RGB (если необходимо)
        image = image.convert('RGB')
        
        # Сохранение в буфер памяти (необязательно, можно сразу передать в pytesseract)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        img = Image.open(img_byte_arr)
        # Извлечение текста
        extracted_text = pytesseract.image_to_string(img, lang='rus')
        return extracted_text
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None


if __name__ == "__main__":
    contracts_txt = ""
    main_folder = Path(r"D:\Program Files\Desktop")

    for file in main_folder.iterdir():
        if file.is_file() and file.suffix == ".png" and "Screenshot_" in file.name:
            contract_names = extract_text_from_image_file(file)

            for contract in contract_names.split('\n'):
                if contract:
                    contracts_txt += f"{contract}\n"

            contracts_txt += "\n"

    print(contracts_txt)
    with open("contracts.txt", "w", encoding="utf-8") as file:
        file.write(contracts_txt)

