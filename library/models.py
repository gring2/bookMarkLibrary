import json


class Category:
    def __init__(self, id:  str, name, sub: list):
        self.id = id
        self.name = name
        self.sub = sub


class SnapShot:
    def __init__(self, id: str,  url, img) -> None:
        super().__init__()
        self.id = id
        self.url = url
        self.img = img

    def __repr__(self):
        return json.dumps(self.__dict__)


