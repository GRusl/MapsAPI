import requests

from io import BytesIO

MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"


def get_img(map_params_user=None):
    if map_params_user is None:
        map_params_user = {}

    map_params = {
        "l": "map"
    }

    return BytesIO(requests.get(MAP_API_SERVER, params=map_params | map_params_user).content)
