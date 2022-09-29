from datetime import datetime

import requests

from environs import Env

env = Env()
env.read_env()


# TODO поправить загрузку, чтобы загружалась определенное количество фотографий
def get_links_nasa_epic(quantity_epic=10) -> list:
    """Функция получает ссылки на фотографии EPIC c сайта NASA.
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
