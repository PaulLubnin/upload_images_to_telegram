import argparse
import random

import requests

from boot_scripts import creating_spacex_data, save_image

API_SPACEX_URL = 'https://api.spacexdata.com/v5/launches/'


def get_random_launch_id() -> str:
    """Функция для получения рандомного идентификатора запуска."""

    response = requests.get(API_SPACEX_URL)
    response.raise_for_status()
    launches = response.json()
    launch_ids = [launch['id'] for launch in launches]

    return random.choice(launch_ids)


def get_spacex_launch_images(launch_id: str = None):
    """Функция сохраняет фотографии запуска ракет c сайта SpaceX."""

    api_spacex_url = f'{API_SPACEX_URL}{launch_id}' \
        if launch_id else f'{API_SPACEX_URL}{get_random_launch_id()}'
    response = requests.get(api_spacex_url)
    response.raise_for_status()
    if not response.json()['links']['flickr']['original']:
        raise SystemExit('Selected launch has no photos')
    all_spacex = creating_spacex_data(response.json())
    save_image(all_spacex)


def main():
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
        get_spacex_launch_images()
        print('Rocket launch photos saved in "images/spacex" folder')

    elif args.id_launch:
        print(f'Uploading photos SpaceX launch - {args.id_launch}')
        get_spacex_launch_images(args.id_launch)
        print('Rocket launch photos saved in "images/spacex" folder')

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
