from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, decode_token

from logger_db import LoggerDB

from models import *


class LoggerApi(Resource):
    @jwt_required()
    def get(self):
        token = request.headers['Authorization'].replace('Bearer ', '')
        decode = decode_token(token)
        user_id = decode['sub']['id']
        list_logs = db.session.query(Log).filter_by(user_id=user_id).distinct()
        logs = []
        for log in list_logs:
            log = {
                'log': log.log,
                'time_created': log.time_created
            }
            logs.append(log)
        LoggerDB.log_user_by_id(user_id, f'"GET {request.url}" 200 -')
        return jsonify(logs)
