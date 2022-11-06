from flask_jwt_extended import decode_token
from models import Log


class LoggerDB(object):
    @staticmethod
    def log_user_by_token(token, message):
        decode = decode_token(token)
        Log.create_log(decode['sub']['id'], message)

    @staticmethod
    def log_user_by_id(user_id, message):
        Log.create_log(user_id, message)
