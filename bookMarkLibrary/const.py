kind = {
    'category': {
        'code': '1',
        'name': 'category'
    },
    'book_mark': {
        'code': '2',
        'name': 'book mark'

    }
}


def register_const():
    from flask import g
    g.kind = kind


