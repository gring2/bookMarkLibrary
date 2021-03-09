from datetime import datetime
from flask_security import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
import library.models as library_model
from bookMarkLibrary.database import db
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    __password = db.Column(db.String(255), name='password')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    bookmarks = relationship('BookMark', back_populates='holder', lazy='dynamic')

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

    def create_bookmarks(self, *args: library_model.BookMark):
            try:
                self.bookmarks.extend([*args])
            except Exception as e:
                import logging
                logging.error('seeror', e)
            db.session.add(self)

    def as_dict(self):
        return {'email': self.email}
