from datetime import datetime

import requests


# TODO сделать чтобы загружались фотографии по ID или рандомный вариант
def get_links_spacex_launch_images(id_launch=None) -> list:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX.
     Возвращает список словарей с 'id_launch', 'image_url' и 'date'."""

    all_launch_photos = []
    api_spacex = f'https://api.spacexdata.com/v5/launches/{id_launch}' \
        if id_launch else 'https://api.spacexdata.com/v5/launches/'
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
