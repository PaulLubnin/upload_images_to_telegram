import random

import requests

import photo_upload


def get_random_launch_id() -> str:
    """Функция для получения рандомного идентификатора запуска."""

    all_spacex = 'https://api.spacexdata.com/v5/launches/'
    response = requests.get(all_spacex)
    response.raise_for_status()
    launches = response.json()
    launch_ids = [launch['id'] for launch in launches]

    return random.choice(launch_ids)


def get_links_spacex_launch_images(launch_id: str = None) -> list:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX,
     либо по заданному 'id', либо случайный вариант. Возвращает список из урлов."""

    api_spacex = f'https://api.spacexdata.com/v5/launches/{launch_id}' \
        if launch_id else f'https://api.spacexdata.com/v5/launches/{get_random_launch_id()}'
    response = requests.get(api_spacex)
    response.raise_for_status()
    launch = response.json()

    if not launch['links']['flickr']['original']:
        print('Selected launch has no photos')
    return launch['links']['flickr']['original']


if __name__ == '__main__':
    photo_upload.main_spacex()
