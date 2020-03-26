import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename, sanitize_filepath
from urllib.parse import urljoin
import json


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


def download_image(url, filename, folder='images/'):
    response_image = requests.get(url, allow_redirects=False)
    response_image.raise_for_status()

    correct_filename = sanitize_filename(filename)
    correct_folder = sanitize_filepath(folder)
    correct_path = os.path.join(correct_folder, correct_filename)

    os.makedirs(correct_folder, exist_ok=True)

    if response_image.status_code == 200:
        with open(correct_path, 'wb') as file:
            file.write(response_image.content)

    return correct_path


def main():
    pattern = 'http://tululu.org/b{}/'

    descriptions = []

    for book_id in range(1, 2):
        url_book = pattern.format(book_id)

        response = requests.get(url_book, allow_redirects=False)
        response.raise_for_status()

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            title, author = soup.find('div', id='content').find('h1').text.split(' \xa0 :: \xa0 ')
            url_txt = f'http://tululu.org/txt.php?id={book_id}'
            book_path = download_txt(url_txt, f"{book_id}.{title}")

            image_src = soup.find('div', class_='bookimage').find('img')['src']
            url_image = urljoin(pattern, image_src)
            name_image = image_src.split('/')[-1]
            image_path = download_image(url_image, name_image)

            comments = []
            comments_soup = soup.find_all('div', class_='texts')
            for comment in comments_soup:
                comments.append(comment.span.string)

            genres = []
            genres_soup = soup.find('span', class_='d_book').find_all('a')
            for genre in genres_soup:
                genres.append(genre.text)

            description = {
                "title": title,
                "author": author,
                "image_path": image_path,
                "book_path": book_path,
                "genres": genres,
                "comments": comments
            }
            descriptions.append(description)

    with open("description.json", "w", encoding='utf8') as file:
        json.dump(descriptions, file, ensure_ascii=False, indent=4)

    with open("description.json", "r", encoding='utf8') as my_file:
        description = json.load(my_file)
        print(description)



if __name__ == '__main__':
    main()
