import json
import traceback


def get_data_obj(path):
    data = {}
    try:
        with open(path, "rt") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(traceback.format_exc())  # いつものTracebackが表示される

    finally:
        return data


def write_json_file(path, data):
    with open(path, "wt") as file:
        json.dump(data, file)
