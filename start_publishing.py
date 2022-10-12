import argparse
import os
import random
import time
from pathlib import Path

import telegram
from environs import Env


def get_photo_paths() -> list:
    """Функция собирает все пути к фотографиям из папки 'images'."""

    directory = Path.cwd().joinpath('images')
    tree_directories = os.walk(directory)

    all_photos = [Path.cwd().joinpath(adress).joinpath(name)
                  for adress, dirs, files in tree_directories
                  for name in files]

    return all_photos


def send_photo(tg_bot_token: str, tg_chat_id: str, publication_frequency: int = 14400):
    """Функция отправляет по одной фотографии в чат через указанный интервал."""

    bot = telegram.Bot(token=tg_bot_token)
    photos = get_photo_paths()

    with open(random.choice(photos), 'rb') as file:
        try:
            bot.send_photo(chat_id=tg_chat_id,
                           photo=file)
        except telegram.error.BadRequest as error:
            print(error)
        time.sleep(publication_frequency)


def main():
    """Функция запуска бота из командной строки."""

    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog='start_publishing.py',
        description='Publication of photos in a telegram channel')
    parser.add_argument(
        '-p', '--periodicity', default=14400, type=int,
        help='Photo posting frequency. Seconds.')
    args = parser.parse_args()

    print(f'Photos are posted every {args.periodicity} seconds.')

    while True:
        try:
            send_photo(env('TG_BOT_TOKEN'), env('TG_CHAT_ID'), args.periodicity)
        except telegram.error.NetworkError:
            print('No network connection.')
            time.sleep(60)


if __name__ == '__main__':
    main()
