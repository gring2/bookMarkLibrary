from models import User
from tests.base import BaseTestCase

from library.models import BookMark, Tag
from library import contract


class LibraryContractTest(BaseTestCase):
    def test_register_bookmark_and_tag(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertEqual(b1, u1.bookmarks[0])
        self.assertEqual(2, len(u1.bookmarks[0].tags))

    def test_register_bookmark_and_tag_rollback_on_error(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag()
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertIsNone(u1.bookmarks[0].id)
        self.assertEqual(0, Tag.query.count())
        self.assertEqual(0, BookMark.query.count())
