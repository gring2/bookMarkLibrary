from bookMarkLibrary.database import db
from models import User
from library.models import BookMark, Tag


def register_bookmark_and_tag(user: User, bookmark: BookMark, *args: [Tag]):
    try:
        bookmark.tags.extend([*args])
        user.create_bookmarks(bookmark)
        db.session.commit()
    except Exception:
        db.session.rollback()
