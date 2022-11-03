from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import *


class AuthUserApi(Resource):
    def post(self):
        c = Auth()
        c.create_user()
        return jsonify({'message': 'New user created!'})


class AuthLoginApi(Resource):
    def post(self):
        c = Auth()
        args = c.login()
        return args


class Auth(object):
    @staticmethod
    def create_user():
        data = request.json
        username = data['username']
        password = data['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def login():
        data = request.json
        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).one_or_none()
        if user is not None and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.username)
            return jsonify({
                'message': 'Success',
                'token': access_token
            })
        else:
            return jsonify({
                'message': 'Login error'
            })
