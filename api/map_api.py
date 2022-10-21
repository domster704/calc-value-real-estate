import requests
from flask import jsonify
from flask_restful import Resource

# api ключ, который я получил в личном кабинете apidata.mos.ru
API_KEY = "bdfe5153e721f1cc0afb699312765f70"


class MapOfBuildingManager(Resource):
    """
    Получаем на вход 1 параметр - global_id.
    global_id - идентификатор строения, благодаря, которому можно найти
    это здание на карте.
    global_id можно взять из аттрибута id тега <td> из списка участков
    ссылка - https://data.mos.ru/opendata/60562
    :param global_id: str
    """

    def get(self, global_id: str):
        response = requests.get(self.__getMapDataLink(global_id))
        return jsonify(response.json())

    @staticmethod
    def __getMapDataLink(global_id):
        return f"https://apidata.mos.ru/v1/mapfeatures/060562?versionNumber=3&releaseNumber=822&rowId={global_id}&api_key={API_KEY}"
