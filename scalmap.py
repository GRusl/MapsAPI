import requests


def selection_scale(response):
    if isinstance(response, requests.models.Response):
        # Преобразуем ответ в json-объект
        json_response = response.json()

    # Получаем первый топоним из ответа геокодера.
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]

    return toponym_coodrinates.split(" ")  # Долгота и широта
