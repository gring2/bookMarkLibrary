import json
import traceback
from library.models import SnapShot

def fetch_data_obj(path):
    data = {}
    try:
        with open(path, "rt") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(traceback.format_exc())  # いつものTracebackが表示される

    finally:
        if 'thumbnails' not in data:
            data['thumbnails'] = []
        else:
            for idx, thumbnail in enumerate(data['thumbnails']):
                tmp = SnapShot(**thumbnail)
                data['thumbnails'][idx] = tmp
        return data


def write_json_file(path, data):
    with open(path, "wt") as file:
        json.dump(data, file, cls=JSONEncoder)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
