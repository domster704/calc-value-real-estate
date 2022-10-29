import time

import bs4
import cloudscraper
from flask import request, jsonify
from flask_restful import Resource


class CianParserApi(Resource):
    def get(self):
        args = request.json
        cianParser = CianParser(args)
        return cianParser.parse()


class CianParser(object):
    def __init__(self, dictWithData: dict):
        self.__cloudscraper = cloudscraper.create_scraper()
        self.__cloudscraper.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        self.__geocodeID = 0
        self.__listOfFlatsID = []
        self.__listOfFlatsLink = []
        self.__listOfFlatParams = []

        self.__address = dictWithData["address"]
        self.__rooms = dictWithData["room"]
        self.__segment = dictWithData["segment"]
        self.__floor = dictWithData["floor"]
        self.__material = dictWithData["material"]

    def parse(self):
        self.__geoID("г. Москва, ул. Ватутина")
        self.__calcFlatsLinksAndIDs()
        # for i in self.__listOfFlatsLink:
        #     self.__parsePage(i)
        return self.__listOfFlatParams

    def __geoID(self, addressInputted: str):
        """
        :param addressInputted: адрес, который мы получаем из таблицы на фронте.
        e.g. address = г. Москва, ул. Ватутина, д. 11
        """

        def getCoord():
            """
            :return: список из координат формата [x, y]
            """
            linkForGetCoord = f"https://www.cian.ru/api/geo/geocode-cached/?request={addressInputted}"
            responseForGetCoord = self.__cloudscraper.get(linkForGetCoord)
            return responseForGetCoord.json()["items"][0]

        data = getCoord()
        linkForGetGeoID = "https://www.cian.ru/api/geo/geocoded-for-search/"
        responseForGetGeoID = self.__cloudscraper.post(linkForGetGeoID, json={
            "Lng": data["coordinates"][0],
            "Lat": data["coordinates"][1],
            "Kind": data["kind"],
            "Address": data["text"]
        })

        self.__geocodeID = responseForGetGeoID.json()["details"][1]["id"]

    def __calcFlatsLinksAndIDs(self):
        """
        Функция для нахождения id и ссылки квартир по заданному адресу.
        """

        houseMaterialsId = {
            "Неважно": 0,
            "Кирпичный": 1,
            "Монолитный": 2,
            "Панельный": 3,
        }

        segmentId = {
            "Старый жилой фонд": 1,
            "Новостройка": 2,
            "Современное жильё": 2
        }

        linkOfOffers = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"
        # TODO: сделать возможность изменять кол-во комнат
        responseOfOffers = self.__cloudscraper.post(linkOfOffers, json={
            "jsonQuery": {
                "_type": "flatsale",
                "engine_version": {
                    "type": "term",
                    "value": 2
                },
                "geo": {
                    "type": "geo",
                    "value": [{
                        "type": "street",
                        "id": self.__geocodeID
                    }]
                },
                "room": {
                    "type": "terms",
                    "value": [
                        self.__rooms
                    ]
                },
                "house_material": {
                    "type": "terms",
                    "value": [
                        houseMaterialsId[self.__material]
                    ]
                },
                "region": {
                    "type": "terms",
                    "value": [
                        1
                    ]
                },
                "building_status": {
                    "type": "term",
                    "value": segmentId[self.__segment]
                },
                "floor": {
                    "type": "range",
                    "value": {
                        "gte": 0,
                        "lte": self.__floor
                    }
                }
            }
        })

        for elem in responseOfOffers.json()["data"]["offersSerialized"]:
            data = {
                "price": elem["bargainTerms"]["price"],
                "room": elem["roomsCount"],
                "floor": elem["floorNumber"],
                "maxFloor": elem["building"]["floorsCount"],
                "material": elem["building"]["materialType"],
                "buildingData": elem["building"]
            }
            self.__listOfFlatParams.append(data)

            # idOfFlat = elem["id"]
            # self.__listOfFlatsID.append(idOfFlat)
            # self.__listOfFlatsLink.append(f"https://www.cian.ru/sale/flat/{idOfFlat}")

    def __parsePage(self, link: str):
        """
        Функция для получения данных о квартире посредством парсинга.
        :param link: ссылка на квартиру на сайте cian
        """

        page = self.__cloudscraper.get(link).text
        soup = bs4.BeautifulSoup(page, "html.parser")

        data = {}

        price = soup.find("span", {"itemprop": "price"})
        flatParams = soup.find_all("div", {"class": "a10a3f92e9--info-value--bm3DC"})
        flatParamsTitle = soup.find_all("div", {"class": "a10a3f92e9--info-title--JWtIm"})

        if flatParams == [] or flatParamsTitle == [] or price is None:
            return

        data["price"] = price.text.replace(" ", "")[:-1]

        for i in range(len(flatParams)):
            value = flatParams[i].text
            title = flatParamsTitle[i].text
            res = ""
            if title not in ["Этаж"]:
                res = value.replace(" ", "")[:-2]
            elif title == "Этаж":
                res = list(map(int, value.replace(" ", "").split("из")))
            elif title == "Построен":
                res = value.replace(" ", "")
            data[title] = res
        self.__listOfFlatParams.append(data)
        time.sleep(1)


if __name__ == "__main__":
    c = CianParser()
    c.parse()
