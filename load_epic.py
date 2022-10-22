import requests
from environs import Env

from boot_scripts import creating_epic_data, save_image


def get_nasa_epic_images(nasa_api_key):
    """Функция сохраняет фотографии EPIC c сайта NASA."""

    api_epic_url = 'https://epic.gsfc.nasa.gov/api/natural'
    params = {
        'api_key': nasa_api_key,
    }
    response = requests.get(api_epic_url, params=params)
    response.raise_for_status()
    all_epics = [creating_epic_data(elem) for elem in response.json()]
    save_image(all_epics)


def main():
    """Функция запуска скрипта из командной строки."""

    env = Env()
    env.read_env()

    print(f'Uploading EPIC photos')
    get_nasa_epic_images(env('NASA_API_KEY'))
    print('NASA photos saved in "images/epic/" folder')


if __name__ == '__main__':
    main()
