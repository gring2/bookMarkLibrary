import json
from tests.base import client


def dumps(dicts):
    return json.dumps(dicts)


def loads(serialized):
    return json.loads(serialized)


def post(url, data, **kw):
    return client.post(url, content_type='application/json', data=dumps(data), **kw)


def get(url, **kw):
    return client.get(url, content_type='application/json', **kw)


def patch(url, data, **kw):
    return client.patch(url, content_type='application/json', data=dumps(data), **kw)


def delete(url, **kw):
    return client.delete(url, content_type='application/json', **kw)


def put(url, **kw):
    return client.put(url, content_type='application/json', data=dumps(kw['data']), **kw)
