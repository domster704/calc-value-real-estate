from flask import jsonify, request
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello Grisha (George)!'})

    def post(self):
        arg = request.json
        print(arg)
        return jsonify("xd")


class HelloTest(Resource):
    def get(self):
        return jsonify({'message': 'Test'})
