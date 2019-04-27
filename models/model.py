from datetime import datetime
from flask_security import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_security.utils import hash_password

from bookMarkLibrary.database import db


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    __password = db.Column(db.String(255), name='password')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @hybrid_property
    def roles(self):
        return []

    @roles.setter
    def roles(self, role):
        pass

    @hybrid_property
    def active(self):
        return True

    @active.setter
    def active(self, active):
        pass

    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password


class IDPublisher(db.Model):

    __tablename__ = 'id_publisher'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
