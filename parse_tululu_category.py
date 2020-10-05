import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tululu import download_txt, download_image, try_get_response
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Парсер онлайн библиотеки tululu.org')

    parser.add_argument('--start_page', type=int, default=1,
                        help='Стартовая страница категории(включительно)')
    parser.add_argument('--end_page', type=int, default=3,
                        help='Конечная страница категории(не включительно)')

    parser.add_argument('--dest_folder', type=str, default=None,
                        help='Путь к каталогу с результатами парсинга("--dest_folder имяПапки")')
    parser.add_argument('--json_path', type=str, default=None,
                        help='Путь к *.json файлу("--json_path имяПапки")')

    parser.add_argument('--skip_imgs', action='store_true',
                        help='Не скачивать картинки')
    parser.add_argument('--skip_txt', action='store_true',
                        help='Не скачивать книги')

    parser.add_argument('--category', type=str, default='l55',
                        help='Категория (пример из "tululu.org/fantastic/" вписать => "--category fantastic")')
    return parser.parse_args()


def get_texts(texts_soup):
    texts = []
    for text_soup in texts_soup:
        texts.append(text_soup.text)
    if not texts:
        return None
    return texts


def main():
    base_url = 'https://tululu.org/'
    args = get_args()

    descriptions = []
    for category_page in range(args.start_page, args.end_page):
        category_url = urljoin(base_url, args.category + '/' + str(category_page))

        category_response = try_get_response(category_url)
        if not category_response.status_code == 200:
            break

        category_soup = BeautifulSoup(category_response.text, 'lxml')
        books = category_soup.select('#content .d_book')

        for book in books:
            author, title = book.a['title'].split(' - ', maxsplit=1)

            book_id = book.a['href']
            book_url = urljoin(base_url, book_id)
            book_response = try_get_response(book_url)
            if not category_response.status_code == 200:
                break

            book_soup = BeautifulSoup(book_response.text, 'lxml')
            comments = get_texts(book_soup.select('.texts .black'))
            genres = get_texts(book_soup.select('span.d_book a'))

            if args.skip_txt:
                book_path = None
            else:
                try:
                    txt_href = book_soup.select_one('[href*="txt"]')['href']
                    txt_url = urljoin(base_url, txt_href)
                    book_path = download_txt(txt_url, title, folder=args.dest_folder)
                except TypeError:
                    continue

            if args.skip_imgs:
                image_path = None
            else:
                image_src = book.img['src']
                image_url = urljoin(base_url, image_src)
                image_name = image_src.split('/')[-1]
                image_path = download_image(image_url, image_name, folder=args.dest_folder)

            description = {
                "title": title,
                "author": author,
                "image_path": image_path,
                "book_path": book_path,
                "genres": genres,
                "comments": comments
            }
            descriptions.append(description)

    if args.dest_folder is not None:
        os.makedirs(args.dest_folder, exist_ok=True)
        dest_path = os.path.join(args.dest_folder, "description.json")
    else:
        dest_path = "description.json"

    if args.json_path is not None:
        os.makedirs(args.json_path, exist_ok=True)
        dest_path = os.path.join(args.json_path, "description.json")

    with open(dest_path, "w", encoding='utf8') as file:
        json.dump(descriptions, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
