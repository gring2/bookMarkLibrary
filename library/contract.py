import os
import time
from flask import current_app as app
from bookMarkLibrary.database import db
from handlers.screenshot_handler import resize_img
from library.models import BookMark, Tag
from bookMarkLibrary.const import ALLOWED_EXTENSIONS

"""library.contract
function sets which models communicate for library manipulating purpose
"""


def register_bookmark_and_tag(user, bookmark: BookMark, *args: [Tag]):
    try:
        with db.session.no_autoflush:
            bookmark.tags.extend([*args])
            user.create_bookmarks(bookmark)
            db.session.commit()
    except Exception as e:
        import logging
        import traceback
        logging.error(traceback.format_exc())
        db.session.rollback()


def change_thumbnail(bookmark: BookMark, file):
    if file and __allowed_file(file.filename):
        ts = time.time()
        img_name = str(int(ts)) + file.filename
        path = os.path.join(app.config['STORAGE_PATH'], img_name)
        file.save(path)
        resize_img(path)

        try:

            bookmark.img = img_name
            db.session.add(bookmark)
            db.session.commit()

        except Exception:
            os.remove(path)
            db.session.rollback()


def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
