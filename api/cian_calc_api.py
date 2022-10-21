import bs4
import cloudscraper
from flask_restful import Resource


class CianCalc(Resource):
    """
    Данный класс выполняет функцию парсера калькулятора от cian для определения цены квартиры
    """

    def __init__(self):
        # Объект для парсинга, который позволяет обходить ситуации, связанные с возвращением страницы с надписью
        # "Ваш браузер проверяется, подождите 5 секунд"
        self.scraper = cloudscraper.create_scraper()

    def get(self):
        pass

    def getPrice(self):
        """
        Функция для расчёта цены квартиры на основе уже готового cian калькулятора.
        Так как API для этого калькулятора нет в открытом доступе, то будем использовать эту функцию.
        :return: цена квартиры
        """

        # Входные данные для расчёта цены квартиры
        # Данные о регионе
        territoryData = {
            "country": "Россия",
            "region": "%2C".join(["Удмуртская", "Республика"]),
            "city": "Ижевск",
            "street": "%2C".join(["улица", "Максима", "Горького"]),
        }
        # Базовые данные для квартиры
        flatData = {
            "area": "44",
            "roomsCount": "2"
        }
        reqStr = "%2C%20".join(territoryData.values())

        # Лямбда-функция для вычисления ссылки с итоговой цной
        mainLinkWithPrice = lambda \
                estimationID: f"""https://www.cian.ru/kalkulator-nedvizhimosti/?address={reqStr}%2C%20151&totalArea={flatData["area"]}&roomsCount={flatData["roomsCount"]}&estimationId={estimationID}&valuationType=sale"""
        linkWithPrice = mainLinkWithPrice(self.__getEstimationID())

        content = self.scraper.get(linkWithPrice)
        soup = bs4.BeautifulSoup(content.text, "html.parser")

        # Поиск тега span с определённым классом, который содержит цену
        res = soup.find("span",
                        class_="f0b5faa8cb--color_black_100--kPHhJ f0b5faa8cb--lineHeight_46px--gxGWe f0b5faa8cb--fontWeight_bold--ePDnv f0b5faa8cb--fontSize_38px--Q0xUb f0b5faa8cb--display_block--pDAEx f0b5faa8cb--text--g9xAG f0b5faa8cb--text_letterSpacing__normal--xbqP6")

        # Так как {self.scraper.get(...)} не всегда возвращает то, что надо, поэтому будет повторно вызывать методы
        # для поиска тега с ценой
        while res is None:
            content = self.scraper.get(linkWithPrice)
            soup = bs4.BeautifulSoup(content.text, "html.parser")
            res = soup.find("span",
                            class_="f0b5faa8cb--color_black_100--kPHhJ f0b5faa8cb--lineHeight_46px--gxGWe f0b5faa8cb--fontWeight_bold--ePDnv f0b5faa8cb--fontSize_38px--Q0xUb f0b5faa8cb--display_block--pDAEx f0b5faa8cb--text--g9xAG f0b5faa8cb--text_letterSpacing__normal--xbqP6")
        return res.text

    def __getEstimationID(self):
        """
        Функция для вычисления estimation, который в будущем будет использован в качестве параметра для ссылки с ценой квартиры.
        :return: estimationID - идентификатор в бд cian для расчёта цены
        """

        # Структура JSON для отправки запроса
        null = None
        estimationReq = {
            "infrastructure": [
                "school",
                "kindergarten",
                "polyclinic",
                "shop"
            ],
            "yearRelease": 2020,
            "isAgent": "false",
            "valuationReason": "buy",
            "isOfferParamsKnown": "true",
            "houseMaterialType": null,
            "floorMax": null,
            "floor": null,
            "ceilingHeight": null,
            "loggiaOrBalcony": null,
            "windowsView": null,
            "repair": null,
            "repairAge": null,
            "withAppliancesOrFurniture": [
                "appliances",
                "furniture"
            ],
            "timeToCenter": null,
            "wantRealtor": "false",
            "houseId": 6985488,
            "area": 44,
            "roomsCount": 2
        }
        url = "https://ud-api.cian.ru/price-estimator/v2/save-user-estimation/"
        response = self.scraper.post(url, json=estimationReq)
        return response.json()["estimationId"]


if __name__ == "__main__":
    s = CianCalc()
    print(s.getPrice())
