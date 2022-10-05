import argparse
import os
import time
from pathlib import Path

import telegram
from environs import Env

env = Env()
env.read_env()


def send_photo(tg_bot_token, tg_chat_id, publication_frequency: int = 14400):
    """Функция отправляет фотографии в чат."""

    bot = telegram.Bot(token=tg_bot_token)
    directory = Path.cwd().joinpath('images')
    tree_directories = os.walk(directory)

    for address, dirs, files in tree_directories:
        for name in files:
            with open(os.path.join(address, name), 'rb') as image:
                bot.send_photo(chat_id=tg_chat_id,
                               photo=image)
                time.sleep(publication_frequency)


def main():
    """Функция запуска бота из командной строки."""

    tg_bot_token = env('TG_BOT_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')

    parser = argparse.ArgumentParser(
        prog='start_publishing.py',
        description='Publication of photos in a telegram channel')
    parser.add_argument(
        '-p', '--periodicity', default=14400, type=int,
        help='Photo posting frequency. Seconds. Max frequency 4 hors (14400 sec).')
    args = parser.parse_args()

    if args.periodicity == 14400:
        print(f'Photos are posted every 4 hours')
        send_photo(tg_bot_token, tg_chat_id)

    else:
        print(f'Photos are posted every {args.periodicity} seconds.')
        send_photo(tg_bot_token, tg_chat_id, args.periodicity)


if __name__ == '__main__':
    main()
