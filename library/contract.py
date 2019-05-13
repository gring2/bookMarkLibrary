from bookMarkLibrary.database import db
from library.models import BookMark, Tag


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
