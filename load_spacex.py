import argparse
import random
import sys
from datetime import datetime

from boot_scripts import load_photo, get_json

API_SPACEX_URL = 'https://api.spacexdata.com/v5/launches/'


def get_random_launch_id() -> str:
    """Функция для получения рандомного идентификатора запуска."""

    launches = get_json(API_SPACEX_URL)
    launch_ids = [launch['id'] for launch in launches]

    return random.choice(launch_ids)


def get_links_spacex_launch_images(launch_id: str = None) -> dict:
    """Функция вытаскивает ссылки на картинки c сайта SpaceX,
     либо по заданному 'id', либо случайный вариант. Возвращает словарь с 'date' и 'image_url'."""

    api_spacex_url = f'{API_SPACEX_URL}{launch_id}' \
        if launch_id else f'{API_SPACEX_URL}{get_random_launch_id()}'
    launch = get_json(api_spacex_url)

    if not launch['links']['flickr']['original']:
        print('Selected launch has no photos')
        sys.exit()
    else:
        return {'date': datetime.fromisoformat(launch['date_local']).strftime('%Y-%m-%d'),
                'image_url': launch['links']['flickr']['original']}


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
        load_photo(get_links_spacex_launch_images())
        print('Rocket launch photos saved in "images/spacex" folder')
    elif args.id_launch:
        print(f'Uploading photos SpaceX launch - {args.id_launch}')
        load_photo(get_links_spacex_launch_images(args.id_launch))
        print('Rocket launch photos saved in "images/spacex" folder')
    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
