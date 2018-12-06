import json
import traceback
from library.models import SnapShot, Category


# make dicts from json file
def fetch_data_obj(path):
    data = {}
    """
        return dicts :
            # root node's name of thumbnails is 'root'
            # sub can have SnapShotObj and CategoryObj
            
            {'thumbnails': CategoryObj{'id': str, 'name':str, sub: list }}
            
        __object_hook_mapping (dicts): return object mapped dicts
    """

    def __object_hook_mapping(o: dict)->dict:
        try:
            if 'thumbnails' in o:
                tmp = Category(**o['thumbnails'])
                o['thumbnails'] = tmp
            elif 'sub' in o:
                o['sub'] = __mapping_to_sub_object(o['sub'])
        except KeyError:
            print(traceback.format_exc())  #
        finally:
            return o

    def __mapping_to_sub_object(l: list)->list:
        try:
            for idx, item in enumerate(l):
                tmp = None
                if 'url' in item:
                    tmp = SnapShot(**item)
                elif 'sub' in item:
                    tmp = Category(**item)

                if tmp is not None:
                    l[idx] = tmp
        except KeyError:
            print(traceback.format_exc())  #
        finally:
            return l


    try:
        with open(path, "rt") as file:
            data = json.load(file, object_hook=__object_hook_mapping)
    except FileNotFoundError:
        print(traceback.format_exc())  # いつものTracebackが表示される

    finally:
        # if thumbnails is not in data initialize thumbnails list
        if 'thumbnails' not in data:
            data['thumbnails'] = Category(id='0', name='root', sub=[])

    return data


def write_json_file(path: str, data: dict):
    with open(path, "wt") as file:
        json.dump(data, file, cls=JSONEncoder)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
