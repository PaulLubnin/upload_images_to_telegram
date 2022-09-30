import random
from datetime import datetime

import requests


def get_links_spacex_launch_images(id_launch: str = None) -> dict:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX,
     либо по заданному 'id', либо случайный вариант.
     Возвращает список словарей с 'id_launch', 'image_url' и 'date'."""

    selected_launch = []
    api_spacex = f'https://api.spacexdata.com/v5/launches/{id_launch}' \
        if id_launch else 'https://api.spacexdata.com/v5/launches/'
    response = requests.get(api_spacex)
    response.raise_for_status()

    if not id_launch:
        for launch in response.json():
            if launch['links']['flickr']['original']:
                one_launch = {
                    'id_launch': launch['id'],
                    'date': datetime.fromisoformat(launch['date_local']).strftime('%Y-%m-%d'),
                    'image_url': launch['links']['flickr']['original']
                }
                selected_launch.append(one_launch)
        selected_launch = random.choice(selected_launch)
    else:
        if not response.json()['links']['flickr']['original']:
            print('Selected launch has no photos')
        else:
            one_launch = {
                'id_launch': response.json()['id'],
                'date': datetime.fromisoformat(response.json()['date_local']).strftime('%Y-%m-%d'),
                'image_url': response.json()['links']['flickr']['original']
            }
            selected_launch = one_launch

    return selected_launch
