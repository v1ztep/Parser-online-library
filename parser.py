import os
import requests


os.makedirs("books", exist_ok=True)

pattern = 'http://tululu.org/txt.php?id={}'

for i in range(1, 11):
    url = pattern.format(i)

    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    
    if response.status_code == 200:
        filename = 'id{}.txt'.format(i)
        with open('books/{}'.format(filename), 'w') as file:
            file.write(response.text)

