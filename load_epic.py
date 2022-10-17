import argparse

import requests
from environs import Env

from boot_scripts import create_data, save_image


def get_links_nasa_epic(nasa_api_key, quantity_epic: int = None):
    """Функция сохраняет фотографии EPIC c сайта NASA."""

    api_epic_url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': nasa_api_key,
    }
    response = requests.get(api_epic_url, params=params)
    response.raise_for_status()
    all_epics = create_data(response.json())
    save_image(all_epics)


def main():
    """Функция запуска скрипта из командной строки."""

    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog='load_epic.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qe', '--quantity_epic', type=int, default=1,
                        help='Quantity of EPIC photos uploaded.')
    args = parser.parse_args()

    if args.quantity_epic:
        print(f'Uploading EPIC photos')
        get_links_nasa_epic(env('NASA_API_KEY'))
        print('NASA photos saved in "images/nasa/epic/" folder')

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
