import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

pattern = 'http://tululu.org/l55/{}/'

for category_page in range(1, 11):
    url_category = pattern.format(category_page)

    response = requests.get(url_category, allow_redirects=False)
    response.raise_for_status()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.find_all('div', class_='bookimage')
        for book in books:
            href = book.a['href']
            url_book = urljoin(url_category, href)
            print(url_book)