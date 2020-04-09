# Парсер книг с сайта tululu.org

Скрипт скачивает книги с сайта tululu.org.

## Требования к окружению

python 3.7

## Установка

Требуется установка дополнительных библиотек, файл requirements.txt с зафиксированными версиями пакетов.
  - Для установки необходимых библиотек следует в терминале прописать `pip install -r requirements.txt`.

## Запуск парсера

Для запуска парсера следует в терминале прописать `python parse_tululu_category.py`.
  - По умолчанию будут скачиваться все книги всей категории "Научная фантастика", через аргументы (описание ниже) можно выбрать свои условия загрузки. 

### Аргументы

Для выставления своих условий загрузки книг можно использовать аргументы:

  - `--start_page` - Стартовая страница категории(включительно), необходимо указать номер страницы после аргумента. По умолчанию выставлено "1".
  - `--end_page` - Конечная страница категории(не включительно), необходимо указать номер страницы после аргумента. По умолчанию выставлено "9999".
  - `--dest_folder` - Путь к каталогу с результатами парсинга, необходимо указать путь после аргумента(`--dest_folder имяПапки/`). По умолчанию скачивает в корень.
  - `--json_path` - Путь к *.json файлу, необходимо указать путь после аргумента (`--json_path имяПапки/`). По умолчанию скачивает в корень.
  - `--skip_imgs` - Не скачивать картинки.
  - `--skip_txt` - Не скачивать книги.
  - `--category` - Также возможно указать свой жанр книг, для этого необходимо на сайте [tululu.org](http://tululu.org/) зайти в раздел интересующего жанра с книгами и скопировать название категории из адресной строки сайта
   (пример в разделе "Фантастика и фэнтези" в адресной строке `tululu.org/fantastic/` скопировать => `fantastic`) и вставить после указания аргумента (`--category fantastic`). По умолчанию выставлено "l55" (Научная фантастика).

Пример: `python parse_tululu_category.py --start_page 1 --end_page 2 --dest_folder result/` скачает все книги первой страницы категории "Научная фантастика" в папку с именем "result".