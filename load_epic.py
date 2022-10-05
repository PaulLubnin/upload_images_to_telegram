import random
from datetime import datetime

import requests

import photo_upload


def get_links_nasa_epic(nasa_api_key, quantity_epic: int = None) -> list:
    """Функция получает ссылки на фотографии EPIC c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    all_epic = []
    api_nasa = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': nasa_api_key,
    }
    response = requests.get(api_nasa, params=params)
    response.raise_for_status()

    for epic in response.json():
        one_epic = {
            'date': datetime.fromisoformat(epic['date']).strftime('%Y-%m-%d'),
            'image_url': f'https://epic.gsfc.nasa.gov/archive/natural/'
                         f'{datetime.fromisoformat(epic["date"]).strftime("%Y/%m/%d")}/png/{epic["image"]}.png'
        }
        all_epic.append(one_epic)

    if not quantity_epic:
        return all_epic
    return random.sample(all_epic, quantity_epic)


if __name__ == '__main__':
    photo_upload.main_epic()
