from __future__ import annotations
import os
import traceback
import time
import logging
from flask import url_for, current_app as app
from bookMarkLibrary.database import db
from handlers.thumbnail_handler import ThumbnailHandler
from bookMarkLibrary.const import ALLOWED_EXTENSIONS
from handlers.screenshot_handler import resize_img
from utils.url_utils import get_http_format_url

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
    deleted_at = db.Column(db.DateTime)
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
    _url = db.Column(db.String(255), nullable=False)
    img = db.Column(db.String(255))
    name = db.Column(db.String(255))

    parent_id = db.Column(db.Integer)
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

        if not self.img:
            return url_for('static', filename='img/blank.png')

        elif os.path.exists(app.config['STORAGE_PATH'] + '/' + self.img) is True:
            return url_for('storage', filename=self.img)

        return self.img

    @property
    def url(self):
        return get_http_format_url(self._url)

    @url.setter
    def url(self, url):
        self._url = url

    def makeup(self):
        handler = ThumbnailHandler(self.url)
        file_name, name = handler.create_thumbnail()

        self.img = file_name
        self.name = name

        return self

    def save(self):

        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception:
            logging.error(traceback.format_exc())
            db.session.rollback()

    # need to be moved 
    def change_thumbnail(self, file):
        if file and self.__allowed_file(file.filename):
            ts = time.time()
            img_name = str(int(ts)) + file.filename
            path = os.path.join(app.config['STORAGE_PATH'], img_name)
            file.save(path)
            resize_img(path)

            try:

                self.img = img_name

                db.session.add(self)
                db.session.commit()

            except Exception:
                os.remove(path)
                db.session.rollback()

    def __allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

