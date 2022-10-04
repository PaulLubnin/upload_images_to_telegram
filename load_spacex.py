import random

import requests

import photo_upload


def get_random_id_launch() -> str:
    """Функция для получения рандомного идентификатора запуска."""

    all_spacex = 'https://api.spacexdata.com/v5/launches/'
    response = requests.get(all_spacex)
    response.raise_for_status()
    launches = response.json()
    id_launches = [launch['id'] for launch in launches]

    return random.choice(id_launches)


def get_links_spacex_launch_images(id_launch: str = None) -> list:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX,
     либо по заданному 'id', либо случайный вариант. Возвращает список из урлов."""

    api_spacex = f'https://api.spacexdata.com/v5/launches/{id_launch}' \
        if id_launch else f'https://api.spacexdata.com/v5/launches/{get_random_id_launch()}'
    response = requests.get(api_spacex)
    response.raise_for_status()
    launch = response.json()

    if not launch['links']['flickr']['original']:
        print('Selected launch has no photos')
    return launch['links']['flickr']['original']


if __name__ == '__main__':
    photo_upload.main_spacex()
