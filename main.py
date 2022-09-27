import random
from pathlib import Path

import requests


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


def get_and_save_images(array: list):
    """Функция выбирает случайным образом один запуск, затем создает и сохраняет папку с картинками запуска. """

    one_launch = random.choice(array)
    image_directory = Path.cwd().joinpath(f"image/{one_launch['id_launch']}")
    Path(image_directory).mkdir(parents=True, exist_ok=True)

    for link_number, link in enumerate(one_launch['links_image'], 1):
        response = requests.get(link)
        response.raise_for_status()
        with open(f'{image_directory}/space_{link_number}.jpg', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    api_spacex = 'https://api.spacexdata.com/v5/launches/'
    get_and_save_images(get_all_image_links(api_spacex))
