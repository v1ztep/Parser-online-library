import os
import requests
from pathvalidate import sanitize_filename, sanitize_filepath
import hashlib


def get_hash_sum(response):
    if response.status_code == 200:
        md5 = hashlib.md5(response.content)
        return md5.hexdigest()
    return


def download_txt(url, filename, folder=None):
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

    if response_txt.status_code == 200:
        correct_filename = f"{get_hash_sum(response_txt)}_{sanitize_filename(filename)}.txt"
        correct_folder = sanitize_filepath(os.path.join(folder, 'books'))
        correct_path = os.path.join(correct_folder, correct_filename)

        os.makedirs(correct_folder, exist_ok=True)

        with open(correct_path, 'w', encoding='utf8') as file:
            file.write(response_txt.text)

        return correct_path
    return


def download_image(url, filename, folder=None):
    response_image = requests.get(url, allow_redirects=False)
    response_image.raise_for_status()

    if response_image.status_code == 200:
        correct_filename = f"{get_hash_sum(response_image)}_{sanitize_filename(filename)}"
        correct_folder = sanitize_filepath(os.path.join(folder, 'images'))
        correct_path = os.path.join(correct_folder, correct_filename)

        os.makedirs(correct_folder, exist_ok=True)

        with open(correct_path, 'wb') as file:
            file.write(response_image.content)

        return correct_path
    return
