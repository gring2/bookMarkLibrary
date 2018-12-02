import json
import traceback
from library.models import SnapShot


def fetch_data_obj(path):
    data = {}
    """Example function with types documented in the docstring.

        `PEP 484`_ type annotations are supported. If attribute, parameter, and
        return types are annotated according to `PEP 484`_, they do not need to be
        included in the docstring:

        inner_function:
            __object_hook_mapping (dicts): return object mapped dicts
        """

    def __object_hook_mapping(o: dict)->dict:
        try:
            for idx, thumbnail in enumerate(o['thumbnails']):
                tmp = SnapShot(**thumbnail)
                o['thumbnails'][idx] = tmp
        except KeyError:
            print(traceback.format_exc())  #
        finally:
            return o

    try:
        with open(path, "rt") as file:
            data = json.load(file, object_hook=__object_hook_mapping)
    except FileNotFoundError:
        print(traceback.format_exc())  # いつものTracebackが表示される

    finally:
        # if thumbnails is not in data initialize thumbnails list
        if 'thumbnails' not in data:
            data['thumbnails'] = []

    return data


def write_json_file(path: str, data: dict):
    with open(path, "wt") as file:
        json.dump(data, file, cls=JSONEncoder)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
