import json
from bookMarkLibrary.database import db


class Category(db.Model):
    """
        :private property __sub: list to insert child_elements 
        :property sub: list @read_only property to represent children

    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def sub(self):
        return self.__sub    

    @sub.setter
    def sub(self, sub_list: list):
        def get_id(elem):
            return elem.id
        sub_list.sort(key=get_id)
        self.__sub = sub_list


class SnapShot(db.Model):

    __tablename__ = "snapshots"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    url = db.Column(db.String(255))
    img = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)

    def __repr__(self):
        return json.dumps(self.__dict__)


