import time

import bs4
import cloudscraper
from flask_restful import Resource


class CianParserApi(Resource):
    def get(self):
        pass

    def post(self):
        pass


class CianParser(object):
    def __init__(self):
        self.cloudscraper = cloudscraper.create_scraper()
        self.geoID = 0
        self.listOfFlatsID = []
        self.listOfFlatsLink = []

    def parse(self):
        self.__geoID("г. Москва, ул. Ватутина")
        self.__calcFlatsLinksAndIDs()
        self.__parsePage(self.listOfFlatsLink[0])

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
            responseForGetCoord = self.cloudscraper.get(linkForGetCoord)
            return responseForGetCoord.json()["items"][0]

        data = getCoord()
        linkForGetGeoID = "https://www.cian.ru/api/geo/geocoded-for-search/"
        responseForGetGeoID = self.cloudscraper.post(linkForGetGeoID, json={
            "Lng": data["coordinates"][0],
            "Lat": data["coordinates"][1],
            "Kind": data["kind"],
            "Address": data["text"]
        })

        self.geoID = responseForGetGeoID.json()["details"][1]["id"]

        # link = f"https://api.cian.ru/geo-suggest/v2/suggest/?offerType=flat&query={address}&regionId=1&dealType=sale&source=serp"
        # link = f"https://api.cian.ru/geo-suggest/v2/{1}-komnata/suggest/?offerType=flat&query=2&regionId=1&dealType=sale&source=serp"
        # response = self.cloudscraper.get(link)
        # print(response.text)
        # print(response.json()["data"]["suggestions"]["newbuildings"]["items"][0]["id"])
        # geoID = response.json()["data"]["suggestions"]["newbuildings"]["items"][0]["id"]

    def __calcFlatsLinksAndIDs(self):
        """
        Функция для нахождения id и ссылки квартир по заданному адресу.
        """
        linkOfOffers = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"
        # TODO: сделать возможность изменять кол-во комнат
        responseOfOffers = self.cloudscraper.post(linkOfOffers, json={
            "jsonQuery": {
                "_type": "flatsale",
                "engine_version": {
                    "type": "term",
                    "value": 2
                },
                "geo": {
                    "type": "geo",
                    "value": [
                        {
                            "type": "street",
                            "id": self.geoID
                        }
                    ]
                },
                "room": {
                    "type": "terms",
                    "value": [
                        2
                    ]
                },
                "region": {
                    "type": "terms",
                    "value": [
                        1
                    ]
                }
            }
        })
        for elem in responseOfOffers.json()["data"]["offersSerialized"]:
            idOfFlat = elem["id"]
            self.listOfFlatsID.append(idOfFlat)
            self.listOfFlatsLink.append(f"https://www.cian.ru/sale/flat/{idOfFlat}")

    def __parsePage(self, link: str):
        """
        Функция для получения данных о квартире посредством парсинга.
        :param link: ссылка на квартиру на сайте cian
        :return: словарь с характеристиками квартиры
        """

        # Вынужденная мера ждать 4 секунды, чтобы сайт не понял, что мы "робот"
        time.sleep(4)
        page = self.cloudscraper.get(link).text
        soup = bs4.BeautifulSoup(page, "html.parser")

        data = {}
        a = soup.find("span", {"itemprop": "price"})
        # flatParams = soup.find_all("div", {"class": "a10a3f92e9--info-value--bm3DC"})
        flatParams = soup.find_all("div", {"data-testid": "object-summary-description-value"})

        data["square"] = flatParams[0].text.replace(" ", "")[:-3]
        data["liveSquare"] = flatParams[1].text.replace(" ", "")[:-3]
        data["kitchen"] = flatParams[2].text.replace(" ", "")[:-3]
        data["floor"], data["maxFloor"] = flatParams[3].text.replace(" ", "").split("из")
        data["year"] = flatParams[4].text.replace(" ", "")
        data["price"] = a.text.replace(" ", "")[:-1]

        print(data)


if __name__ == "__main__":
    c = CianParser()
    c.parse()
