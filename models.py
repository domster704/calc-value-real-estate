from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
import datetime

db = SQLAlchemy()
jwt = JWTManager()


class User(db.Model):
    __tablename__ = 'gbu_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @staticmethod
    def create_user(username, password):
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


class Log(db.Model):
    __tablename__ = 'dbu_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('gbu_user.id'),
                        nullable=False)
    log = db.Column(db.String(255), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)

    @staticmethod
    def create_log(user_id, message):
        log = Log(user_id=user_id, log=message)
        db.session.add(log)
        db.session.commit()
