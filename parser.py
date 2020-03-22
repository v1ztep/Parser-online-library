import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath


def download_txt(url, filename, folder='books/'):
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
    correct_folder = sanitize_filepath(folder)
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)

    if response_txt.status_code == 200:
        with open(correct_path, 'w') as file:
            file.write(response_txt.text)

    return correct_path


pattern = 'http://tululu.org/b{}/'

for book_id in range(1, 11):
    url_book = pattern.format(book_id)

    response = requests.get(url_book, allow_redirects=False)
    response.raise_for_status()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title, author = soup.find('div', id='content').find('h1').text.split(' \xa0 :: \xa0 ')
        url_txt = f'http://tululu.org/txt.php?id={book_id}'
        download_txt(url_txt, f"{book_id}.{title}")


# os.makedirs("books", exist_ok=True)
#
# pattern = 'http://tululu.org/txt.php?id={}'
#
# for id in range(1, 11):
#     url = pattern.format(id)
#
#     response = requests.get(url, allow_redirects=False)
#     response.raise_for_status()
#
#     if response.status_code == 200:
#         filename = 'id{}.txt'.format(id)
#         with open('books/{}'.format(filename), 'w') as file:
#             file.write(response.text)
