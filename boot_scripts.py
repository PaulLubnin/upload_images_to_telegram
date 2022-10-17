import sys
from datetime import datetime
from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def get_project_name(url: str) -> str:
    """Функция вытаскивает и возвращает из урла название проекта."""

    unq_url = unquote(url)
    unq_split = urlsplit(unq_url)[1]
    prefix = unq_split.split('.')[0]
    project_name = 'spacex' if (prefix != 'epic' and prefix != 'apod') else prefix
    return project_name


def get_file_extension(url: str) -> str:
    """Функция вытаскивает из урла расширение файла"""

    unq_url = unquote(url).replace(' ', '_')
    unq_split = urlsplit(unq_url)[2]
    extension = splitext(unq_split)[1]
    return extension


def create_path(url: str, url_number: str, photo_date: str) -> Path:
    """Функция создает папку и возвращает путь файла"""

    save_folder = Path.cwd() / 'images' / get_project_name(url) / photo_date
    file_name = f'{get_project_name(url)}_{url_number}_{photo_date}{get_file_extension(url)}'
    Path(save_folder).mkdir(parents=True, exist_ok=True)
    return save_folder / file_name


def save_image(array: list):
    """Функция обрабатывает список словарей и сохраняет фотографии."""

    for url_number, url in enumerate(array, 1):
        save_path = create_path(url['image_url'], str(url_number), url['date'])
        response = requests.get(url['image_url'])
        response.raise_for_status()
        photo = response.content
        with open(save_path, 'wb') as file:
            file.write(photo)


def create_data(json) -> list:
    """Функция создает список словарей из входящего JSON. Словарь: {'date': , 'image_url': }."""

    if isinstance(json, list):
        data = []
        for elem in json:
            if elem.get('media_type'):
                if elem['media_type'] == 'image':
                    data.append({
                        'date': datetime.fromisoformat(elem['date']).strftime('%Y-%m-%d'),
                        'image_url': elem['url']
                    })
            else:
                data.append({
                    'date': datetime.fromisoformat(elem['date']).strftime('%Y-%m-%d'),
                    'image_url': f'https://epic.gsfc.nasa.gov/archive/natural/'
                                 f'{datetime.fromisoformat(elem["date"]).strftime("%Y/%m/%d")}'
                                 f'/png/{elem["image"]}.png'
                })
        return data

    if isinstance(json, dict):
        if not json['links']['flickr']['original']:
            print('Selected launch has no photos')
            sys.exit()
        else:
            data = [{'date': datetime.fromisoformat(json['date_local']).strftime('%Y-%m-%d'),
                     'image_url': elem} for elem in json['links']['flickr']['original']]
            return data
