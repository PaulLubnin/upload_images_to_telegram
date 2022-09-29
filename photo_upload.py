import argparse
import random
from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests

from load_apod import get_links_nasa_apod
from load_epic import get_links_nasa_epic
from load_spacex import get_links_spacex_launch_images


def get_file_extension(url: str):
    """Функция вытаскивает из урла расширение файла"""

    return splitext(urlsplit(unquote(url).replace(' ', '_'))[2])[1]


def images_directory(path: str):
    """Функция создает директорию, куда будут сохраняться картинки и возвращает её путь."""

    directory = Path.cwd().joinpath(f"{path}")
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


def save_image(array: list):
    """Функция сохраняет картинки."""

    if array[0].get('id_launch'):
        one_launch = random.choice(array)
        path = f'images/spacex/{one_launch["date"]}'
        for link_number, link in enumerate(one_launch['image_url'], 1):
            response = requests.get(link)
            response.raise_for_status()
            file_extension = get_file_extension(link)
            with open(f"{images_directory(path)}/space_{link_number}{file_extension}", 'wb') as file:
                file.write(response.content)
        print('Rocket launch photos saved in "images/spacex" folder ')
    else:
        for elem_number, elem in enumerate(array, 1):
            response = requests.get(elem['image_url'])
            response.raise_for_status()
            file_extension = get_file_extension(elem['image_url'])
            if not elem.get('image_name'):
                path = 'images/nasa/apod'
                with open(f'{images_directory(path)}/apod_{elem_number}_{elem["date"]}{file_extension}', 'wb') as file:
                    file.write(response.content)
            else:
                path = 'images/nasa/epic'
                with open(f'{images_directory(path)}/epic_{elem_number}_{elem["date"]}{file_extension}', 'wb') as file:
                    file.write(response.content)
        print('NASA photos saved in "images/nasa" folder')


def main():
    """Функция запуска программы из командной строки."""

    parser = argparse.ArgumentParser(
        prog='photo_upload.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-s', '--source', choices=['spacex', 'apod', 'epic'], default='nothing', type=str,
                        help='Sources: "spacex", "apod", "epic".')
    parser.add_argument('-id', '--id_launch', type=str, default='random',
                        help='ID SpaceX launch')
    parser.add_argument('-qa', '--quantity_apod', type=int, default=30,
                        help='Quantity of APOD photos uploaded')
    parser.add_argument('-qe', '--quantity_epic', type=int, default=10,
                        help='Quantity of EPIC photos uploaded')
    args = parser.parse_args()

    if args.source == 'nothing':
        print('You must specify the source. It can be either "spacex" or "apod" or "epic".')

    elif args.source == 'apod' and args.quantity_apod == 30:
        print('Uploading 30 APOD photos')
        save_image(get_links_nasa_apod())
    elif args.source == 'apod' and args.quantity_apod:
        print(f'Uploading {args.quantity_apod} APOD photos')
        save_image(get_links_nasa_apod(args.quantity_apod))

    # TODO поправить загрузку, чтобы загружалась определенное количество фотографий
    elif args.source == 'epic' and args.quantity_epic == 10:
        print('Uploading 30 EPIC photos')
        save_image(get_links_nasa_epic())
    elif args.source == 'epic' and args.quantity_epic:
        print(f'Uploading {args.quantity_epic} EPIC photos')
        save_image(get_links_nasa_epic(args.quantity_epic))

    # TODO сделать чтобы загружались фотографии по ID или рандомный вариант
    elif args.source == 'spacex' and args.id_launch == 'random':
        print('Uploading photos random SpaceX launch')
        save_image(get_links_spacex_launch_images())
    elif args.source == 'spacex' and args.id_launch:
        print(f'Uploading photos SpaceX launch - {args.id_launch}')
        save_image(get_links_spacex_launch_images(args.id_launch))

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
