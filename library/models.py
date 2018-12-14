import json

class Category:
    """
        :private property __sub: list to insert child_elements 
        :property sub: list @read_only property to represent children

    """

    def __init__(self, id:  str, name, parent_id: str):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.__sub = []

    @property
    def sub(self):
        return self.__sub    

    @sub.setter
    def sub(self, list: list):
        self.__sub = list


class SnapShot:
    def __init__(self, id: str,  url, img, parent_id: str) -> None:
        super().__init__()
        self.id = id
        self.url = url
        self.img = img
        self.parent_id = parent_id

    def __repr__(self):
        return json.dumps(self.__dict__)


