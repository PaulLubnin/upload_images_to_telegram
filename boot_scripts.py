from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def get_project_name(url: str) -> str:
    """Функция вытаскивает из урла название проекта NASA"""

    unq_url = unquote(url)
    unq_split = urlsplit(unq_url)[1]
    project_name = unq_split.split('.')[0]
    return project_name


def get_file_extension(url: str) -> str:
    """Функция вытаскивает из урла расширение файла"""

    unq_url = unquote(url).replace(' ', '_')
    unq_split = urlsplit(unq_url)[2]
    extension = splitext(unq_split)[1]
    return extension


def create_path(url: str, url_number: str, photo_date: str) -> Path:
    """Функция обрабатывает урл, создает папку и возвращает путь файла"""

    project_name = 'spacex' if (get_project_name(url) != 'epic' and get_project_name(url) != 'apod') \
        else get_project_name(url)
    save_folder = Path.cwd() / 'images' / project_name / photo_date if project_name == 'spacex' \
        else Path.cwd() / 'images' / 'nasa' / project_name
    file_name = project_name + '_' + url_number + '_' + photo_date + get_file_extension(url)
    Path(save_folder).mkdir(parents=True, exist_ok=True)
    return save_folder / file_name


def save_image(url: str, url_number: str, photo_date: str):
    """Функция сохраняет фотографии"""

    save_path = create_path(url, photo_date, url_number)
    response = requests.get(url)
    response.raise_for_status()
    photo = response.content
    with open(save_path, 'wb') as file:
        file.write(photo)


def load_photo(array: dict, link_number=1):
    """Функция загружает фотографии"""

    if type(array['image_url']) == list:
        for url_number, url in enumerate(array['image_url'], 1):
            save_image(url, array['date'], str(url_number))

    if type(array['image_url']) == str:
        save_image(array['image_url'], array['date'], str(link_number))
