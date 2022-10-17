import argparse
import random
from datetime import datetime

import requests
from environs import Env

from boot_scripts import load_photo


def get_links_nasa_epic(nasa_api_key, quantity_epic: int = None) -> list:
    """Функция получает ссылки на фотографии EPIC c сайта NASA.
    Возвращает список словарей с 'image_url' и 'date'."""

    api_epic_url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': nasa_api_key,
    }
    response = requests.get(api_epic_url, params=params)
    response.raise_for_status()
    epics = response.json()
    all_epic = [{'date': datetime.fromisoformat(epic['date']).strftime('%Y-%m-%d'),
                 'image_url': f'https://epic.gsfc.nasa.gov/archive/natural/'
                              f'{datetime.fromisoformat(epic["date"]).strftime("%Y/%m/%d")}/png/{epic["image"]}.png'}
                for epic in epics]

    if not quantity_epic:
        return all_epic
    return random.sample(all_epic, quantity_epic)


def main():
    """Функция запуска скрипта из командной строки."""

    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog='load_epic.py',
        description='Loading images from the selected source.'
    )
    parser.add_argument('-qe', '--quantity_epic', type=int, default=3,
                        help='Quantity of EPIC photos uploaded.')
    args = parser.parse_args()

    if args.quantity_epic:
        print(f'Uploading {args.quantity_epic} EPIC photos')
        for link_number, image_link in enumerate(get_links_nasa_epic(env('NASA_API_KEY'), args.quantity_epic), 1):
            load_photo(image_link, link_number)
        print('NASA photos saved in "images/nasa/epic/" folder')

    else:
        print('Unknown command.')


if __name__ == '__main__':
    main()
