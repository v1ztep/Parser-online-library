import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tululu import download_txt, download_image
import re
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Парсер онлайн библиотеки tululu.org')

    parser.add_argument('--start_page', type=int, default=1,
                        help='Стартовая страница категории(включительно)')
    parser.add_argument('--end_page', type=int, default=9999,
                        help='Конечная страница категории(не включительно)')

    parser.add_argument('--dest_folder', type=str, default='',
                        help='Путь к каталогу с результатами парсинга("имяПапки")')
    parser.add_argument('--json_path', type=str, default='',
                        help='Путь к *.json файлу("имяПапки")')

    parser.add_argument('--skip_imgs', action='store_true',
                        help='Не скачивать картинки')
    parser.add_argument('--skip_txt', action='store_true',
                        help='Не скачивать книги')

    parser.add_argument('--category', type=str, default='l55',
                        help='Категория (пример из "tululu.org/fantastic/" внести => "fantastic")')
    return parser.parse_args()


def get_texts(soup_texts):
    texts = []
    for soup_text in soup_texts:
        texts.append(soup_text.text)
    return texts


def main():
    base_url = 'http://tululu.org/{}/{}'
    args = get_args()

    descriptions = []
    for category_page in range(args.start_page, args.end_page):
        category_url = base_url.format(args.category, category_page)

        response_category = requests.get(category_url, allow_redirects=False)
        response_category.raise_for_status()

        if not response_category.status_code == 200:
            break

        soup_category = BeautifulSoup(response_category.text, 'lxml')
        books = soup_category.select('#content .d_book')

        for book in books:
            author, title = book.a['title'].split(' - ', maxsplit=1)

            image_src = book.img['src']
            url_image = urljoin(base_url, image_src)
            name_image = image_src.split('/')[-1]
            if args.skip_imgs:
                image_path = ''
            else:
                image_path = download_image(url_image, name_image, folder=args.dest_folder)

            book_id = re.findall(r'\d+', book.a['href'])[0]
            url_txt = f'http://tululu.org/txt.php?id={book_id}'
            if args.skip_txt:
                book_path = ''
            else:
                book_path = download_txt(url_txt, title, folder=args.dest_folder)

            url_book = f'http://tululu.org/b{book_id}/'
            response_book = requests.get(url_book, allow_redirects=False)
            response_book.raise_for_status()

            if response_book.status_code == 200:
                soup_book = BeautifulSoup(response_book.text, 'lxml')
                comments = get_texts(soup_book.select('.texts .black'))
                genres = get_texts(soup_book.select('span.d_book a'))

            description = {
                "title": title,
                "author": author,
                "image_path": image_path,
                "book_path": book_path,
                "genres": genres,
                "comments": comments
            }
            descriptions.append(description)


    dest_path = os.path.join(args.dest_folder, "description.json")

    if args.dest_folder:
        os.makedirs(args.dest_folder, exist_ok=True)

    if args.json_path:
        dest_path = os.path.join(args.json_path, "description.json")
        os.makedirs(args.json_path, exist_ok=True)

    with open(dest_path, "w", encoding='utf8') as file:
        json.dump(descriptions, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
