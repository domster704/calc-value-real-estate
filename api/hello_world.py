from flask import jsonify
from flask_restful import Resource


class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello Grisha (George)!'})


class HelloTest(Resource):
    def get(self):
        return jsonify({'message': 'Test'})
