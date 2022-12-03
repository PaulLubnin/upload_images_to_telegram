from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def get_file_extension(url: str) -> str:
    """Функция вытаскивает из урла расширение файла"""

    unq_url = unquote(url).replace(' ', '_')
    unq_split = urlsplit(unq_url)[2]
    extension = splitext(unq_split)[1]
    return extension


def create_path(url: str, url_number: str, photo_date: str, folder: str) -> Path:
    """Функция создает папку и возвращает путь файла"""

    save_folder = Path.cwd() / 'images' / folder / photo_date
    file_name = f'{folder}_{url_number}_{photo_date}{get_file_extension(url)}'
    Path(save_folder).mkdir(parents=True, exist_ok=True)
    return save_folder / file_name


def save_image(array: list, folder: str):
    """Функция обрабатывает список словарей и сохраняет фотографии."""

    for url_number, url in enumerate(array, 1):
        save_path = create_path(url['image_url'], str(url_number), url['date'], folder)
        response = requests.get(url['image_url'])
        response.raise_for_status()
        photo = response.content
        with open(save_path, 'wb') as file:
            file.write(photo)
