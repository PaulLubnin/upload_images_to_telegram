import argparse
from datetime import datetime

import requests
from environs import Env

from boot_scripts import save_image


def creating_apod_data(json: dict) -> dict:
    """Функция создаёт словарь {'date': , 'image_url': } из входящего JSON."""

    data = {'date': datetime.fromisoformat(json['date']).strftime('%Y-%m-%d'),
            'image_url': json['url']}
    return data


def get_nasa_apod_images(nasa_api_key, quantity_apod: int):
    """Функция сохраняет фотографии APOD c сайта NASA."""

    api_apod_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_api_key,
        'count': quantity_apod
    }
    response = requests.get(api_apod_url, params=params)
    response.raise_for_status()
    all_apods = [creating_apod_data(elem) for elem in response.json() if elem['media_type'] == 'image']
    save_image(all_apods, folder='apod')


def main():
    """Функция запуска скрипта из командной строки."""

    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog='load_apod.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qa', '--quantity_apod', type=int, default=30,
                        help='Quantity of APOD photos uploaded. Default 30 photo.')
    args = parser.parse_args()

    if args.quantity_apod:
        print(f'Uploading APOD photos')
        get_nasa_apod_images(env('NASA_API_KEY'), args.quantity_apod)
        print('NASA photos saved in "images/apod/" folder')

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
