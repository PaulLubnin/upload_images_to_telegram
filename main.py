import requests


def get_image():
    url_image = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    response = requests.get(url_image)
    response.raise_for_status()
    return response.content


def save_image():
    filename = 'hubble.jpeg'
    with open(filename, 'wb') as file:
        file.write(get_image())


if __name__ == '__main__':
    save_image()
