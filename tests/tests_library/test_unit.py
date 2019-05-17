from models import User
from tests.base import BaseTestCase

from library.models import BookMark, Tag
from bookMarkLibrary.database import db
from library import contract


class BookmarkTagRelTest(BaseTestCase):
    def test_tag_bookmark_relation(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        b2 = BookMark(url='python.org')
        u1.create_bookmarks(b1, b2)
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')
        b1.tags.extend([t1, t2])
        t2.bookmarks.extend([b1, b2])

        db.session.add_all([u1, b1, b2, t1, t2])
        db.session.commit()

        self.assertEqual(2, len(u1.bookmarks.all()))
        self.assertEqual(u1, b1.holder)
        self.assertEqual(u1, b1.holder)
        self.assertEqual(2, len(b1.tags))
        self.assertEqual(2, len(t2.bookmarks))
        self.assertEqual(1, len(b2.tags))
        self.assertEqual(1, len(t1.bookmarks))


class LibraryContactTest(BaseTestCase):
    def test_register_bookmark_and_tag(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertEqual(b1, u1.bookmarks[0])
        self.assertEqual(2, len(u1.bookmarks[0].tags))

    def test_register_bookmark_and_tag_rollback(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag()
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertIsNone(u1.bookmarks[0].id)
        self.assertEqual(0, Tag.query.count())
        self.assertEqual(0, BookMark.query.count())


