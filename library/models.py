from __future__ import annotations
import os
from flask import url_for, current_app as app
from flask_security import current_user
from bookMarkLibrary.database import db
from handlers.thumbnail_handler import ThumbnailHandler
from utils.url_utils import get_http_format_url
from sqlalchemy_utils import UUIDType
import uuid
from sqlalchemy import Table, text
from sqlalchemy.orm import relationship


association_table = Table('bookmark_tag_rel', db.metadata,
                          db.Column('bookmarks', db.Integer, db.ForeignKey('bookmarks.id')),
                          db.Column('tags', UUIDType(binary=False), db.ForeignKey('tags.id'))
                          )


class BookMark(db.Model):

    __tablename__ = "bookmarks"

    id = db.Column(db.Integer, primary_key=True)
    _url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    img = db.Column(db.String(255))
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    holder = relationship('User', back_populates='bookmarks')
    tags = relationship('Tag', secondary=association_table, back_populates='bookmarks')

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
        current_user.create_bookmarks(self)

    def as_dict(self):
        return {'id': self.id, 'url': self.url, 'name': self.name, 'img': self.img}


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    tag = db.Column(db.String(255), nullable=False, unique=True)
    bookmarks = relationship("BookMark",
                             secondary=association_table,
                             back_populates="tags")

    @classmethod
    def find_or_make(cls, tag):
        obj = cls.query.filter_by(tag=tag).first()
        if obj is None:
            obj = Tag(tag=tag)
        return obj

    @staticmethod
    def conv_tag_str_to_list(tag_str: str):
        tag_inputs = tag_str.split('#')

        tag_inputs.pop(0)

        return tag_inputs

    def as_dict(self):
        return {'id': self.id.__str__(), 'tag': self.tag}

    @classmethod
    def get_lists(cls, ids):
        params = {str(idx): id for idx, id in enumerate(ids)}
        stmt = text('SELECT tags.id as id, tags.tag as tag FROM tags'
                    ' '
                    'JOIN bookmark_tag_rel btr on tags.id = btr.tags'
                    ' '
                    'WHERE btr.bookmarks in (%s)'
                    ' '
                    'GROUP BY tags.id'
                    ' '
                    'ORDER BY tags.id' % ','.join([":" + key for key in params.keys()]))

        stmt = stmt.columns(cls.id, cls.tag)

        stmt = stmt.bindparams(**params)

        return db.session.query(cls).from_statement(stmt).all()
