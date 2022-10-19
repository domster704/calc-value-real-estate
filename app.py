from flask import Flask
from flask_restful import Api
from api.hello_world import HelloWorld, HelloTest
from api.map_api import MapOfBuildingManager
from api.input_data_api import InputDataManager
from api.pdf_file_api import PdfFileManager

app = Flask(__name__)
api = Api(app)

# All routes - (Class, Route)
api_routes = [
    (HelloWorld, '/'),
    (HelloTest, '/a'),
    (MapOfBuildingManager, '/api/getMapCoords/<string:global_id>'),
    (InputDataManager, '/api/getPrice'),
    (PdfFileManager, '/api/getPdfFile'),
]

for i in api_routes:
    api.add_resource(i[0], i[1])

if __name__ == '__main__':
    app.run(debug=True)