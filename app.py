from flask import Flask
from flask_restful import Api

from api.cian_parser_api import CianParserApi

app = Flask(__name__)
api = Api(app)

# All routes - (Class, Route)
api_routes = [
    (CianParserApi, '/api/getCianAnalogs'),
]

for i in api_routes:
    api.add_resource(i[0], i[1])
