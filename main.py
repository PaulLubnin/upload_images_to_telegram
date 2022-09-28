import random
from datetime import datetime
from os.path import splitext
from pathlib import Path
from pprint import pprint
from urllib.parse import urlsplit, unquote

import requests
from environs import Env

env = Env()
env.read_env()


def get_links_nasa_apod() -> list:
    """Функция получает ссылки на фотографии дня c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    all_apod = []
    api_nasa = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': env('API_KEY'),
        'count': 30
    }
    response = requests.get(api_nasa, params=params)
    response.raise_for_status()

    for apod in response.json():
        one_apod = {
            'date': apod['date'],
            'image_url': apod['url']
        }
        all_apod.append(one_apod)

    return all_apod


def get_links_nasa_epic() -> list:
    """Функция получает ссылки на фотографии дня c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    all_epic = []
    api_nasa = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': env('API_KEY'),
    }
    response = requests.get(api_nasa, params=params)
    response.raise_for_status()

    for epic in response.json():
        one_epic = {
            'image_name': epic['image'],
            'date': datetime.fromisoformat(epic['date']).strftime('%Y-%m-%d'),
            'image_url': f'https://epic.gsfc.nasa.gov/archive/natural/'
                         f'{datetime.fromisoformat(epic["date"]).strftime("%Y")}/'
                         f'{datetime.fromisoformat(epic["date"]).strftime("%m")}/'
                         f'{datetime.fromisoformat(epic["date"]).strftime("%d")}/'
                         f'png/{epic["image"]}.png'
        }
        all_epic.append(one_epic)

    return all_epic


def get_links_spacex_launch_images() -> list:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX.
     Возвращает список словарей с 'id_launch', 'image_url' и 'date'."""

    all_launch_photos = []
    api_spacex = 'https://api.spacexdata.com/v5/launches/'
    response = requests.get(api_spacex)
    response.raise_for_status()

    for launch in response.json():
        if launch['links']['flickr']['original']:
            one_launch = {
                'id_launch': launch['id'],
                'date': datetime.fromisoformat(launch['date_local']).strftime('%Y-%m-%d'),
                'image_url': launch['links']['flickr']['original']
            }
            all_launch_photos.append(one_launch)

    return all_launch_photos


def get_file_extension(url: str):
    """Функция вытаскивает из урла расширение файла"""

    return splitext(urlsplit(unquote(url).replace(' ', '_'))[2])[1]


def images_directory(path: str):
    """Функция создает директорию, куда будут сохраняться картинки и возвращает её путь."""

    directory = Path.cwd().joinpath(f"{path}")
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


def save_image(array: list):
    """Функция сохраняет картинки."""

    if array[0].get('id_launch'):
        one_launch = random.choice(array)
        for link_number, link in enumerate(one_launch['image_url'], 1):
            response = requests.get(link)
            response.raise_for_status()
            file_extension = get_file_extension(link)
            path = f'images/spacex/{one_launch["date"]}'
            with open(f"{images_directory(path)}/space_{link_number}{file_extension}", 'wb') as file:
                file.write(response.content)
        print('Фотографии запуска ракет сохранены в папку "images/spacex"')
    else:
        for elem_number, elem in enumerate(array, 1):
            response = requests.get(elem['image_url'])
            response.raise_for_status()
            file_extension = get_file_extension(elem['image_url'])
            path = 'images/nasa'
            with open(f'{images_directory(path)}/apod_{elem_number}_{elem["date"]}{file_extension}', 'wb') as file:
                file.write(response.content)
        print('Фотографии дня сохранены в папку "images/nasa"')


if __name__ == '__main__':
    # save_image(get_links_spacex_launch_images())
    # save_image(get_links_nasa_apod())
    save_image(get_links_nasa_epic())
