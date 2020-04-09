import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tululu import download_txt, download_image
import re
import json
import argparse
from pathvalidate import sanitize_filepath

base_url = 'http://tululu.org/l55/{}'


parser = argparse.ArgumentParser(
    description='Парсер онлайн библиотеки tululu.org'
)
parser.add_argument('--start_page', type=int, default=1,
                    help='Стартовая страница категории')

parser.add_argument('--end_page', type=int, default=9999,
                    help='Конечная страница категории(не включительно)')

parser.add_argument('--dest_folder', type=str, default='',
                    help='Путь к каталогу с результатами парсинга("folder/")')

parser.add_argument('--json_path', type=str, default='',
                    help='Путь к *.json файлу("folder/")')

parser.add_argument('--skip_imgs', action='store_true',
                    help='Не скачивать картинки')

parser.add_argument('--skip_txt', action='store_true',
                    help='Не скачивать книги')

args = parser.parse_args()


if args.start_page > 1:
    count_book = (args.start_page-1) * 25
else:
    count_book = 0

descriptions = []

for category_page in range(args.start_page, args.end_page):
    category_url = base_url.format(category_page)

    response_category = requests.get(category_url, allow_redirects=False)
    response_category.raise_for_status()

    if response_category.status_code == 200:
        soup_category = BeautifulSoup(response_category.text, 'lxml')
        books = soup_category.select('#content .d_book')

        for book in books:
            count_book += 1
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
                book_path = download_txt(url_txt, f"{count_book}.{title}", folder=args.dest_folder)

            url_book = f'http://tululu.org/b{book_id}/'
            response_book = requests.get(url_book, allow_redirects=False)
            response_book.raise_for_status()

            comments = []
            genres = []
            if response_book.status_code == 200:
                soup_book = BeautifulSoup(response_book.text, 'lxml')

                comments_soup = soup_book.select('.texts')
                for comment in comments_soup:
                    comments.append(comment.span.text)

                genres_soup = soup_book.select('span.d_book a')
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
    else:
        break


correct_folder = sanitize_filepath(args.dest_folder)
correct_path = os.path.join(correct_folder, "description.json")

if args.dest_folder:
    os.makedirs(correct_folder, exist_ok=True)

if args.json_path:
    correct_folder = sanitize_filepath(args.json_path)
    correct_path = os.path.join(correct_folder, "description.json")
    os.makedirs(correct_folder, exist_ok=True)

with open(correct_path, "w", encoding='utf8') as file:
    json.dump(descriptions, file, ensure_ascii=False, indent=4)
