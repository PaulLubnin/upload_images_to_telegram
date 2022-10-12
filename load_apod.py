import argparse

import requests
from environs import Env

from boot_scripts import load_photo


def get_links_nasa_apod(nasa_api_key, quantity_apod: int = 30) -> list:
    """Функция получает ссылки на фотографии APOD c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    api_apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_api_key,
        'count': quantity_apod
    }
    response = requests.get(api_apod_url, params=params)
    response.raise_for_status()
    apods = response.json()
    all_apod = [{'date': apod['date'], 'image_url': apod['url']} for apod in apods if apod['media_type'] == 'image']

    return all_apod


def main():
    """Функция запуска скрипта из командной строки."""

    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog='load_apod.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qa', '--quantity_apod', type=int, default=30,
                        help='Quantity of APOD photos uploaded. Max 50 photo.')
    args = parser.parse_args()

    if args.quantity_apod == 30:
        print('Uploading 30 APOD photos')
        for link_number, image_link in enumerate(get_links_nasa_apod(env('NASA_API_KEY')), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/apod/" folder')

    elif 50 >= args.quantity_apod >= 1:
        print(f'Uploading {args.quantity_apod} APOD photos')
        for link_number, image_link in enumerate(get_links_nasa_apod(env('NASA_API_KEY'), args.quantity_apod), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/apod/" folder')

    elif args.quantity_apod > 50:
        print('You can upload up to 50 photos at one time.')

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
