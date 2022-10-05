import requests

import photo_upload


def get_links_nasa_apod(nasa_api_key, quantity_apod: int = 30) -> list:
    """Функция получает ссылки на фотографии APOD c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    all_apod = []
    api_nasa = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_api_key,
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


if __name__ == '__main__':
    photo_upload.main_apod()
