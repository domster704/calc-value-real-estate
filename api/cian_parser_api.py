import cloudscraper
from flask import request, jsonify
from flask_restful import Resource


class CianParserApi(Resource):
    def get(self):
        args = request.json
        cianParser = CianParser(args)
        return jsonify(cianParser.parse())


class CianParser(object):
    def __init__(self, dictWithData: dict):
        self.__cloudscraper = cloudscraper.create_scraper()
        self.__cloudscraper.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
        }
        self.__geocodeID: int = 0
        self.__listOfFlatParams: list = []

        # ------------- Обязательные параметры ---------------
        self.__address: str = "".join(dictWithData["address"].split(',')[:-1])
        self.__rooms: int = dictWithData["room"]
        self.__segment: str = str(dictWithData["segment"]).lower()
        self.__maxFloor: int = dictWithData["maxFloor"]
        self.__material: str = str(dictWithData["material"]).lower()

        # ------------- Корректирующие параметры -------------
        self.__flatFloor: int = dictWithData["correctFloor"]
        self.__flatArea: str = dictWithData["correctArea"]
        self.__flatKitchenFloor: str = dictWithData["correctKitchenArea"]
        self.__flatBalcony: bool = True if str(dictWithData["correctBalcony"]).lower() == "true" else False
        self.__metroTime: int = dictWithData["correctMetroTime"]
        self.__flatSegment: str = self.__segment

        self.__typeOfEvalFloor = CorrectParam.getTypeOfFloor(self.__flatFloor, self.__maxFloor)
        self.__typeOfEvalArea = CorrectParam.getTypeOfFloor(self.__flatFloor, self.__maxFloor)

    def parse(self):
        self.__geoID(self.__address)
        self.__readFlatsParamsFromJson()
        return self.__listOfFlatParams

    def __geoID(self, addressInputted: str):
        """
        :param addressInputted: адрес, который мы получаем из таблицы на фронте.
        e.g. address = г. Москва, ул. Ватутина, д. 11
        """

        def getCoord() -> list:
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

    def __readFlatsParamsFromJson(self):
        """
        Функция, которая считывает данные о квартирах с json файла
        """

        houseMaterialsId = {
            "кирпич": 1,
            "brick": 1,
            "монолит": 2,
            "monolith": 2,
            "панель": 3,
            "panel": 3
        }

        segmentId = {
            "старый жилой фонд": 1,
            "oldhousingstock": 1,
            "современное жильё": 1,
            "modernhousing": 1,
            "новостройка": 2,
            "newbuilding": 2,
        }

        linkOfOffers = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"
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
                        int(self.__rooms)
                    ]
                },
                "house_material": {
                    "type": "terms",
                    "value": [
                        houseMaterialsId[self.__material]
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
                        "lte": self.__maxFloor
                    }
                },
                "region": {
                    "type": "terms",
                    "value": [
                        1
                    ]
                }
            }
        })

        for name in ["offersSerialized", "suggestOffersSerializedList"]:
            for elem in responseOfOffers.json()["data"][name]:
                isThereBalcony: bool = True if type(elem["balconiesCount"]) is int and elem[
                    "balconiesCount"] > 0 else False
                metroTime: int = 100000
                for metroData in elem["geo"]["undergrounds"]:
                    metroTime = min(metroData["time"], metroTime)
                
                data = {
                    # "id": elem["id"],
                    # "buildingData": elem["building"],
                    "address": elem["geo"]["userInput"],
                    "price": elem["bargainTerms"]["price"],
                    "roomsCount": elem["roomsCount"],
                    "floor": elem["floorNumber"],
                    "maxFloor": elem["building"]["floorsCount"],
                    "material": elem["building"]["materialType"],
                    "area": elem["totalArea"],
                    "kitchenArea": elem["kitchenArea"],
                    "balcony": str(isThereBalcony),
                    "metroTime": metroTime,
                    "segment": self.__segment,
                    "typeOfFloor": {
                        "x": self.__typeOfEvalFloor,
                        "y": CianParser.__getTypeOfFloor(elem["floorNumber"], elem["building"]["floorsCount"])
                    },
                    "location": {
                        "lat": str(elem["geo"]["coordinates"]["lat"]),
                        "lng": str(elem["geo"]["coordinates"]["lng"]),
                    }
                }

                self.__listOfFlatParams.append(data)


class CorrectParam(object):
    @staticmethod
    def getTypeOfFloor(floor: int, maxFloor: int) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param floor: этаж квартиры.
        :param maxFloor: этажность дома.
        :return:
        Красных зон нет
        """
        status: int = 0
        percent = int(floor / maxFloor) * 100
        if 30 <= percent <= 70:
            status = 1
        elif percent > 70:
            status = 2
        return status

    @staticmethod
    def getTypeOfArea(area: float) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param area: площадь квартиры.
        :return: status - индекс
        if status in [3, 4, 5], то это красная зона
        """
        status: int = 0
        if 30 <= area <= 50:
            status = 1
        elif 50 < area <= 65:
            status = 2
        elif 65 < area <= 90:
            status = 3
        elif 90 < area <= 120:
            status = 4
        elif area > 120:
            status = 5
        return status

    @staticmethod
    def getTypeOfKitchenArea(kitchenArea: float) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param kitchenArea: площадь кухни
        :return: status - индекс
        Красных зон нет
        """
        status: int = 0
        if 7 <= kitchenArea <= 10:
            status = 1
        elif 10 < kitchenArea <= 15:
            status = 2
        return status

    @staticmethod
    def getTypeOfBalcony(isBalcony: bool) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param isBalcony: наличие балкона в квартире
        :return: status - индекс
        Красных зон нет
        """
        status: int = 1 if isBalcony else 0
        return status

    @staticmethod
    def getTypeOfMetroTime(metroTime: int) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param metroTime: время в минутах до метро.
        :return: status - индекс
        if status in [3, 4, 5], то это красная зона
        """
        status: int = 0
        if 5 <= metroTime <= 10:
            status = 1
        elif 10 < metroTime <= 15:
            status = 2
        elif 15 < metroTime <= 30:
            status = 3
        elif 30 < metroTime <= 60:
            status = 4
        elif 60 < metroTime <= 90:
            status = 5
        return status
