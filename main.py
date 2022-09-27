from pathlib import Path
from pprint import pprint

import requests


def get_all_image_links(link_source: str):
    """Функция вытаскивает ссылки на картинки. Возвращает список словарей с 'id_launch' и 'links_image'."""

    pictures_links = []
    response = requests.get(link_source)
    response.raise_for_status()
    for elem in response.json():
        if elem['links']['flickr']['original']:
            one_launch = {
                'id_launch': elem['id'],
                'links_image': elem['links']['flickr']['original']
            }
            pictures_links.append(one_launch)

    return pictures_links


def get_image(url: str):
    """Функция делает запрос на получение картинки по заданному урлу."""

    response = requests.get(url)
    response.raise_for_status()
    return response.content


def save_image(directory_name: str, image_title: str, saved_image: bytes, ):
    """Функция создает папку в проекте и сохраняет в неё картинку."""

    image_directory = Path.cwd().joinpath(directory_name)
    Path(image_directory).mkdir(parents=True, exist_ok=True)
    with open(f'{image_directory}/{image_title}', 'wb') as file:
        file.write(saved_image)


if __name__ == '__main__':
    api_spacex = 'https://api.spacexdata.com/v5/launches/'
    pprint(get_all_image_links(api_spacex))
