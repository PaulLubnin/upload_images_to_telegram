import requests

from environs import Env

env = Env()
env.read_env()


def get_links_nasa_apod(quantity_apod=30) -> list:
    """Функция получает ссылки на фотографии APOD c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    all_apod = []
    api_nasa = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': env('API_KEY'),
        'count': quantity_apod
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
