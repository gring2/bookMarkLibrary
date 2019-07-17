ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
NO_CONTENT = 204
SUCCESS = 200
NOT_FOUND = 404
SERVER_ERROR = 500

def register_const():
    from flask import g
