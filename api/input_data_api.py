from flask import request, jsonify
from flask_restful import Resource


class InputDataManager(Resource):
    """
    Класс-менеджер для вывода цены квартиры/здания по вводимым значениям
    """

    def get(self):
        args = request.json
        testValue = args["test"]
        return jsonify(testValue)

    def post(self):
        pass
