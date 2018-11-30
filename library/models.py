import json


class SnapShot():
    def __init__(self, url, img) -> None:
        super().__init__()
        self.url = url
        self.img = img

    def __repr__(self):
        return json.dumps(self.__dict__)


