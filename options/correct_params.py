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

    @staticmethod
    def getTypeOfStatusFinish(statusFinish: str) -> int:
        """
        Определяет номер строки/столбца для корректировки из таблицы в "Приложении 6"
        :param statusFinish: состояние отделки
        :return: status - индекс
        """
        data: dict = {
            "nofinish": 0,
            "без отделки": 0,
            "econom": 1,
            "муниципальный ремонт": 1,
            "improved": 2,
            "современная отделка": 2
        }

        return data[statusFinish]
