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

    txt_response = requests.get(url, allow_redirects=False)
    txt_response.raise_for_status()

    if txt_response.status_code == 200:
        return

    correct_filename = f"{get_hash_sum(txt_response)}_{sanitize_filename(filename)}.txt"
    if folder is not None:
        correct_folder = sanitize_filepath(os.path.join(folder, 'books'))
    else:
        correct_folder = "books"
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)
    with open(correct_path, 'w', encoding='utf8') as file:
        file.write(txt_response.text)

    return correct_path



def download_image(url, filename, folder=None):
    image_response = requests.get(url, allow_redirects=False)
    image_response.raise_for_status()

    if not image_response.status_code == 200:
        return

    correct_filename = f"{get_hash_sum(image_response)}_{sanitize_filename(filename)}"
    if folder is not None:
        correct_folder = sanitize_filepath(os.path.join(folder, 'images'))
    else:
        correct_folder = "images"
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)
    with open(correct_path, 'wb') as file:
        file.write(image_response.content)

    return correct_path

