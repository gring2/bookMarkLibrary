import json


class Category:
    def __init__(self, id: int, name, sub: list):
        self.id = id
        self.name = name
        self.sub = sub


class SnapShot:
    def __init__(self, url, img, parent: int=None) -> None:
        super().__init__()
        self.url = url
        self.img = img
        self.parent = parent

    def __repr__(self):
        return json.dumps(self.__dict__)


