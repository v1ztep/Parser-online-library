import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    # TODO: Здесь ваша реализация

url = 'http://tululu.org/txt.php?id=1'

filepath = download_txt(url, 'Алиби')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али/би', folder='books/')
print(filepath)  # Выведется books/Алиби.txt

filepath = download_txt(url, 'Али\\би', folder='txt/')
print(filepath)  # Выведется txt/Алиби.txt




# pattern = 'http://tululu.org/b{}/'
#
#
# for id in range(1, 2):
#     url = pattern.format(id)
#
#     response = requests.get(url, allow_redirects=False)
#     response.raise_for_status()
#
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'lxml')
#         title_and_author = soup.find('div', id='content').find('h1').text.split(' \xa0 :: \xa0 ')
#         print('Заголовок:', title_and_author[0])
#         print('Автор:', title_and_author[1])


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

