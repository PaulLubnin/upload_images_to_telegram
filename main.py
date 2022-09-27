from pathlib import Path

import requests


def get_image(url: str):
    """Функция делает запрос на получение картинки по заданному урлу."""

    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def save_image(directory_name: str, image_title: str, saved_image: bytes, ):
    """Функция создает папку в проекте и сохраняет в неё картинку."""

    image_directory = Path.cwd().joinpath(directory_name)
    Path(image_directory).mkdir(parents=True, exist_ok=True)
    with open(f'{image_directory}/{image_title}', 'wb') as file:
        file.write(saved_image)


if __name__ == '__main__':
    url_image = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    image = get_image(url_image)
    filename = 'hubble.jpeg'
    save_image('image', filename, image)
