import argparse
from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests
from environs import Env

import load_apod
import load_epic
import load_spacex

env = Env()
env.read_env()


def get_project_name(url: str) -> str:
    """Функция вытаскивает из урла название проекта NASA"""

    unq_url = unquote(url)
    unq_split = urlsplit(unq_url)[1]
    project_name = unq_split.split('.')[0]
    return project_name


def get_file_extension(url: str) -> str:
    """Функция вытаскивает из урла расширение файла"""

    unq_url = unquote(url).replace(' ', '_')
    unq_split = urlsplit(unq_url)[2]
    extension = splitext(unq_split)[1]
    return extension


def create_path(url: str, url_number: str, photo_date: str) -> Path:
    """Функция обрабатывает урл, создает папку и возвращает путь файла"""

    project_name = 'spacex' if (get_project_name(url) != 'epic' and get_project_name(url) != 'apod') \
        else get_project_name(url)
    save_folder = Path.cwd() / 'images' / project_name / photo_date if project_name == 'spacex' \
        else Path.cwd() / 'images' / 'nasa' / project_name
    file_name = project_name + '_' + url_number + '_' + photo_date + get_file_extension(url)
    Path(save_folder).mkdir(parents=True, exist_ok=True)
    return save_folder / file_name


def get_photo(url: str) -> bytes:
    """Функция делает get запрос и возвращает фотографию"""

    response = requests.get(url)
    response.raise_for_status()
    return response.content


def save_image(url: str, url_number: str, photo_date: str):
    """Функция сохраняет фотографии"""

    save_path = create_path(url, photo_date, url_number)
    photo = get_photo(url)
    with open(save_path, 'wb') as file:
        file.write(photo)


def load_photo(array: dict, link_number=1):
    """Функция загружает фотографии"""

    if type(array['image_url']) == list:
        for url_number, url in enumerate(array['image_url'], 1):
            save_image(url, array['date'], str(url_number))

    if type(array['image_url']) == str:
        save_image(array['image_url'], array['date'], str(link_number))


def main_apod():
    """Функция запуска скрипта из командной строки."""

    nasa_api_key = env('NASA_API_KEY')

    parser = argparse.ArgumentParser(
        prog='load_apod.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qa', '--quantity_apod', type=int, default=30,
                        help='Quantity of APOD photos uploaded. Max 50 photo.')
    args = parser.parse_args()

    if args.quantity_apod == 30:
        print('Uploading 30 APOD photos')
        for link_number, image_link in enumerate(load_apod.get_links_nasa_apod(nasa_api_key), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/apod/" folder')
    elif 50 >= args.quantity_apod >= 1:
        print(f'Uploading {args.quantity_apod} APOD photos')
        for link_number, image_link in enumerate(load_apod.get_links_nasa_apod(nasa_api_key, args.quantity_apod), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/apod/" folder')
    elif args.quantity_apod > 50:
        print('You can upload up to 50 photos at one time.')
    else:
        print('Unknown command.')


def main_epic():
    """Функция запуска скрипта из командной строки."""

    nasa_api_key = env('NASA_API_KEY')

    parser = argparse.ArgumentParser(
        prog='load_epic.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qe', '--quantity_epic', type=int, default=None,
                        help='Quantity of EPIC photos uploaded. Max 12 photo.')
    args = parser.parse_args()

    if args.quantity_epic is None:
        print('Uploading EPIC photos')
        for link_number, image_link in enumerate(load_epic.get_links_nasa_epic(nasa_api_key), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/epic/" folder')
    elif 12 >= args.quantity_epic >= 1:
        print(f'Uploading {args.quantity_epic} EPIC photos')
        for link_number, image_link in enumerate(load_epic.get_links_nasa_epic(nasa_api_key, args.quantity_epic), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/epic/" folder')
    elif args.quantity_epic > 12:
        print('You can upload up to 12 photos at one time')
    else:
        print('Unknown command.')


def main_spacex():
    """Функция запуска скрипта из командной строки."""

    parser = argparse.ArgumentParser(
        prog='load_spacex.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-id', '--id_launch', type=str, default='random',
                        help='ID SpaceX launch')
    args = parser.parse_args()

    if args.id_launch == 'random':
        print('Uploading photos random SpaceX launch')
        load_photo(load_spacex.get_links_spacex_launch_images())
        print('Rocket launch photos saved in "images/spacex" folder')
    elif args.id_launch:
        print(f'Uploading photos SpaceX launch - {args.id_launch}')
        load_photo(load_spacex.get_links_spacex_launch_images(args.id_launch))
        print('Rocket launch photos saved in "images/spacex" folder')
    else:
        print('Unknown command.')
