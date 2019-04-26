import os
from flask import url_for, current_app as app
from bookMarkLibrary.database import db
from handlers.thumbnail_handler import create_thumbnail
import traceback


class Category(db.Model):
    """
        :private property __sub: list to insert child_elements
        :property sub: list @read_only property to represent children

    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    __sub = []

    @property
    def sub(self):
        return self.__sub

    @sub.setter
    def sub(self, sub_list: list):
        def get_id(elem):
            return elem.id
        sub_list.sort(key=get_id)
        self.__sub = sub_list

    @property
    def thumbnail(self):
        if len(self.sub) < 1:
            return url_for('static', filename='img/directory_default.png')
        else:
            return self.sub[0].thumbnail


class BookMark(db.Model):

    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())

    @classmethod
    def remove_last_slash_from_url(cls, url):
        last_char = url[-1:]

        if last_char == '/':
            return url[:-1]
        else:
            return url

    @property
    def thumbnail(self):

        if os.path.exists(app.config['STORAGE_PATH'] + '/' + self.img) is True:
            return url_for('storage', filename=self.img)

        return self.img

    @property
    def name(self):
        return self.url

    def save(self):

        try:
            db.session.add(self)
            db.session.commit()

            file_name = create_thumbnail(self.url)

            if file_name is not False:
                self.img = file_name
                db.session.add(self)
                db.session.commit()
                return self

            else:
                raise Exception

        except Exception:
            print(traceback.format_exc())
            db.session.rollback()
            return False
