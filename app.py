from flask import Flask, render_template, send_from_directory
from flask_restful import Api
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from api.cian_parser_api import CianParserApi
from api.auth import AuthLoginApi
from api.logger_api import LoggerApi
from models import db, jwt
from datetime import timedelta

app = Flask(__name__)
api = Api(app)

DB_URL = 'postgresql+psycopg2://kmggqntwsiumwl:f1ba94a7f9155d2f819e6e53e8e403ec13edde7821c4d2d5548b390d94e5758d@ec2-54-82-205-3.compute-1.amazonaws.com:5432/deqkn4srtrojb6'

app.config['JWT_SECRET_KEY'] = '12345'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=60)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

# All routes - (Class, Route)
api_routes = [
    (CianParserApi, '/api/getCianAnalogs'),
    (AuthLoginApi, '/api/login'),
    (LoggerApi, '/api/logs')
]

for i in api_routes:
    api.add_resource(i[0], i[1])

# API Documentation
SWAGGER_URL = '/api/swagger'
API_URL = '/static/swagger.yaml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Flask Project for LCT hackathon'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Import web routes
from web import app

if __name__ == '__main__':
    app.run()
