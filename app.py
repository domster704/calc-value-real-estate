from flask import Flask
from flask_restful import Api
from api.hello_world import HelloWorld, HelloTest
from api.map_api import MapOfBuildingManager

app = Flask(__name__)
api = Api(app)

# All routes - (Class, Route)
api_routes = [
    (HelloWorld, '/'),
    (HelloTest, '/a'),
    (MapOfBuildingManager, '/getMapCoords/<string:global_id>'),
]

for i in api_routes:
    api.add_resource(i[0], i[1])

if __name__ == '__main__':
    app.run(debug=True)