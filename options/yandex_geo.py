import options.API_KEYS as API_KEYS
import requests


class YandexGeo(object):
    def __init__(self, address: str):
        self.__address = address
        self.__API_KEY = API_KEYS.API_YANDEX_GEO

    def getCoords(self) -> dict:
        """
        Функция для определения координат в виде широты и долготы у дома.
        :return: словарь с координатами дома
        """
        res = requests.get(
            f"https://geocode-maps.yandex.ru/1.x/?format=json&apikey={self.__API_KEY}&geocode={self.__address}")
        data = str(
            res.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]).split()
        return {"location": {
            "lat": data[0],
            "lng": data[1],
        }}
