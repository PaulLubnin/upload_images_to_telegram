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


def get_file_extension(url: str) -> str:
    """Функция вытаскивает из урла расширение файла"""

    return splitext(urlsplit(unquote(url).replace(' ', '_'))[2])[1]


def create_images_directory(path: str):
    """Функция создает директорию, куда будут сохраняться картинки и возвращает её путь."""

    directory = Path.cwd().joinpath(f'{path}')
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


def save_spacex_image(array: dict):
    """Функция сохраняет SpaceX фотографии"""

    save_folder = f'images\\spacex\\{array["date"]}'
    for link_number, link in enumerate(array['image_url'], 1):
        response = requests.get(link)
        response.raise_for_status()
        file_extension = get_file_extension(link)
        save_path = create_images_directory(save_folder)
        with open(f'{save_path}\\space_{link_number}{file_extension}', 'wb') as file:
            file.write(response.content)
    print('Rocket launch photos saved in "images/spacex" folder')


def save_nasa_image(array: list):
    """Функция сохраняет NASA фотографии"""

    for elem_number, elem in enumerate(array, 1):
        response = requests.get(elem['image_url'])
        response.raise_for_status()
        file_extension = get_file_extension(elem['image_url'])
        project_name = urlsplit(unquote(elem["image_url"]))[1].split(".")[0]
        save_folder = f'images\\nasa\\{project_name}'
        save_path = create_images_directory(save_folder)
        with open(f'{save_path}\\{project_name}_{elem_number}_{elem["date"]}{file_extension}', 'wb') as file:
            file.write(response.content)
    print('NASA photos saved in "images/nasa" folder')


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
        save_nasa_image(load_apod.get_links_nasa_apod(nasa_api_key))
    elif 50 >= args.quantity_apod >= 1:
        print(f'Uploading {args.quantity_apod} APOD photos')
        save_nasa_image(load_apod.get_links_nasa_apod(nasa_api_key, args.quantity_apod))
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
        save_nasa_image(load_epic.get_links_nasa_epic(nasa_api_key))
    elif 12 >= args.quantity_epic >= 1:
        print(f'Uploading {args.quantity_epic} EPIC photos')
        save_nasa_image(load_epic.get_links_nasa_epic(nasa_api_key, args.quantity_epic))
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
        save_spacex_image(load_spacex.get_links_spacex_launch_images())
    elif args.id_launch:
        print(f'Uploading photos SpaceX launch - {args.id_launch}')
        save_spacex_image(load_spacex.get_links_spacex_launch_images(args.id_launch))
    else:
        print('Unknown command.')
