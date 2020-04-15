import os
import requests
from pathvalidate import sanitize_filename, sanitize_filepath



def download_txt(url, filename, folder=''):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.

    """

    response_txt = requests.get(url, allow_redirects=False)
    response_txt.raise_for_status()

    correct_filename = f"{sanitize_filename(filename)}.txt"
    correct_folder = sanitize_filepath(folder + 'books/')
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)

    if response_txt.status_code == 200:
        with open(correct_path, 'w', encoding='utf8') as file:
            file.write(response_txt.text)

    return correct_path


def download_image(url, filename, folder=''):
    response_image = requests.get(url, allow_redirects=False)
    response_image.raise_for_status()

    correct_filename = sanitize_filename(filename)
    correct_folder = sanitize_filepath(folder + 'images/')
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)

    if response_image.status_code == 200:
        with open(correct_path, 'wb') as file:
            file.write(response_image.content)

    return correct_path
