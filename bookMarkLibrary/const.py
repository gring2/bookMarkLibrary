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

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def register_const():
    from flask import g
    g.kind = kind
