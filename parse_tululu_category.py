import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tululu import download_txt, download_image
import re
import json

pattern_category = 'http://tululu.org/l55/{}/'
count_book = 0
descriptions = []

for category_page in range(1, 2):
    url_category = pattern_category.format(category_page)

    response = requests.get(url_category, allow_redirects=False)
    response.raise_for_status()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.find('div', id='content').find_all('table', class_='d_book')
        for book in books:
            author, title = book.a['title'].split(' - ', maxsplit=1)

            image_src = book.img['src']
            url_image = urljoin(pattern_category, image_src)
            name_image = image_src.split('/')[-1]
            image_path = download_image(url_image, name_image)

            book_id = re.findall(r'\d+', book.a['href'])[0]
            url_txt = f'http://tululu.org/txt.php?id={book_id}'
            count_book += 1
            book_path = download_txt(url_txt, f"{count_book}.{title}")

            url_book = f'http://tululu.org/b{book_id}/'
            response_book = requests.get(url_book, allow_redirects=False)
            response_book.raise_for_status()

            comments = []
            genres = []
            if response.status_code == 200:
                soup = BeautifulSoup(response_book.text, 'lxml')

                comments_soup = soup.find_all('div', class_='texts')
                for comment in comments_soup:
                    comments.append(comment.span.string)

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

# with open("description.json", "r", encoding='utf8') as my_file:
#     description = json.load(my_file)
#     print(description)



