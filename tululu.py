import os
import requests
from pathvalidate import sanitize_filename, sanitize_filepath
import hashlib


def get_hash_sum(response):
    if not response.status_code == 200:
        return
    md5_hash = hashlib.md5(response.content)
    return md5_hash.hexdigest()


def request_tululu(url):
    response = requests.get(url, allow_redirects=False, timeout=10)
    response.raise_for_status()
    if response.status_code == 301:
        raise requests.HTTPError
    return response


def download_txt(url, filename, folder=None):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.

    """

    try:
        txt_response = request_tululu(url)
    except requests.RequestException:
        return

    if txt_response.status_code != 200:
        return

    correct_filename = f"{get_hash_sum(txt_response)}_{sanitize_filename(filename)}.txt"
    if folder is not None:
        correct_folder = sanitize_filepath(os.path.join(folder, 'books'))
    else:
        correct_folder = "books"
    correct_path = os.path.join(correct_folder, correct_filename).replace("\\", "/")

    os.makedirs(correct_folder, exist_ok=True)
    with open(correct_path, 'w', encoding='utf8', newline='') as file:
        file.write(txt_response.text)

    return correct_path


def download_image(url, filename, folder=None):
    try:
        image_response = request_tululu(url)
    except requests.RequestException:
        return

    if image_response.status_code != 200:
        return

    correct_filename = f"{get_hash_sum(image_response)}_{sanitize_filename(filename)}"
    if folder is not None:
        correct_folder = sanitize_filepath(os.path.join(folder, 'images'))
    else:
        correct_folder = "images"
    correct_path = os.path.join(correct_folder, correct_filename).replace("\\", "/")

    os.makedirs(correct_folder, exist_ok=True)
    with open(correct_path, 'wb') as file:
        file.write(image_response.content)

    return correct_path

