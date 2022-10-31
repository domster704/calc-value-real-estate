from flask import Flask
from flask_restful import Api

from api.input_data_api import InputDataManager
from api.map_api import MapOfBuildingManager
from api.pdf_file_api import PdfFileManager
from api.yandex_parser_api import YandexParserApi
from api.domofond_api_parser import DomofondParserApi

app = Flask(__name__)
app.debug = True
api = Api(app)

# All routes - (Class, Route)
api_routes = [
    (MapOfBuildingManager, '/api/getMapCoords/<string:global_id>'),
    (InputDataManager, '/api/getAnalogs'),
    (PdfFileManager, '/api/getPdfFile'),
    (YandexParserApi, '/api/getAnalogsByYandex'),
    (DomofondParserApi, '/api/getAnalogsByDomofond')
]

for i in api_routes:
    api.add_resource(i[0], i[1])

if __name__ == '__main__':
    app.run()
