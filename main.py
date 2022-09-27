from pathlib import Path

import requests


def get_image():
    url_image = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
    response = requests.get(url_image, headers=headers)
    response.raise_for_status()
    return response.content


def save_image():
    filename = 'hubble.jpeg'
    image_directory = Path.cwd().joinpath('image')
    Path(image_directory).mkdir(parents=True, exist_ok=True)
    with open(f'{image_directory}/{filename}', 'wb') as file:
        file.write(get_image())


if __name__ == '__main__':
    save_image()
