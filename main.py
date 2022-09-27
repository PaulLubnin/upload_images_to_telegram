import random
from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests


def get_file_extension(url: str):
    """Функция вытаскивает из урла расширение файла"""

    return splitext(urlsplit(unquote(url).replace(' ', '_'))[2])[1]


def get_all_image_links(link_source: str):
    """Функция вытаскивает ссылки на картинки. Возвращает список словарей с 'id_launch' и 'links_image'."""

    all_launch_photos = []
    response = requests.get(link_source)
    response.raise_for_status()

    for launch in response.json():
        if launch['links']['flickr']['original']:
            one_launch = {
                'id_launch': launch['id'],
                'links_image': launch['links']['flickr']['original']
            }
            all_launch_photos.append(one_launch)

    return all_launch_photos


def fetch_spacex_random_launch(array: list):
    """Функция выбирает случайным образом один запуск, затем создает и сохраняет папку с картинками запуска. """

    one_launch = random.choice(array)
    image_directory = Path.cwd().joinpath(f"image/{one_launch['id_launch']}")
    Path(image_directory).mkdir(parents=True, exist_ok=True)

    for link_number, link in enumerate(one_launch['links_image'], 1):
        response = requests.get(link)
        response.raise_for_status()
        file_extension = get_file_extension(link)
        with open(f'{image_directory}/space_{link_number}{file_extension}', 'wb') as file:
            file.write(response.content)

    print(f'Фотографии сохранены в папку {image_directory}')


if __name__ == '__main__':
    api_spacex = 'https://api.spacexdata.com/v5/launches/'
    fetch_spacex_random_launch(get_all_image_links(api_spacex))
