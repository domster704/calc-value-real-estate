import options.API_KEYS as API_KEYS
import requests


class YandexGeo(object):
    def __init__(self, address: str):
        self.__address: str = address
        self.__geocode: list = []
        self.__API_KEY: str = API_KEYS.API_YANDEX_GEO

    def getCoords(self) -> dict:
        """
        Функция для определения координат в виде широты и долготы у дома.
        :return: словарь с координатами дома
        """
        res = requests.get(
            f"https://geocode-maps.yandex.ru/1.x/?format=json&apikey={self.__API_KEY}&geocode={self.__address}")
        self.__geocode = str(
            res.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]).split()

        return {"location": {
            "lat": self.__geocode[0],
            "lng": self.__geocode[1],
        }}

    def getDistrict(self) -> str:
        """
        Метод необходимо вызывать только после вызова метод {@link getCoords}
        :return: название района
        """
        s = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.__API_KEY}&geocode={','.join(map(str, self.__geocode))}&kind=district&format=json"
        res = requests.get(s)
        listWithKinds = \
            res.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["Address"][
                "Components"]
        for i in listWithKinds:
            if i["kind"] == "district" and "район" in i["name"]:
                return i["name"]
