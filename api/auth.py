from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import *

from logger_db import LoggerDB


class AuthLoginApi(Resource):
    def post(self):
        c = Auth()
        args = c.login()
        return args


class Auth(object):
    @staticmethod
    def login():
        data = request.json
        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).one_or_none()
        if user is not None and check_password_hash(user.password, password):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            LoggerDB.log_user_by_id(user.id, f'"{request.method} {request.url}" 200 -')
            return {
                       'status': True,
                       'message': 'Success',
                       'token': access_token,
                   }, 200
        else:
            return {
                       'status': False,
                       'message': 'Incorrect login or password!'
                   }, 403
