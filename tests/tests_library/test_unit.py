from sqlalchemy.exc import IntegrityError

from models import User
from tests.base import BaseTestCase

from library.models import BookMark, Tag
from bookMarkLibrary.database import db
from library import contract
from unittest.mock import patch


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

    def test_blank_page_thumbnail(self):
        bookmark = BookMark()
        bookmark.url = 'https://google.com'
        bookmark.makeup()
        bookmark.img = None
        self.assertEqual('/static/img/blank.png', bookmark.thumbnail)

    def test_thumbnail_return_img_value_on_default(self):
        bookmark = BookMark()
        bookmark.url = 'https://google.com'
        bookmark.makeup()
        bookmark.img = 'test'
        self.assertEqual('test', bookmark.thumbnail)

    def test_thumbnail_return_img_path_when_exist(self):
        with patch('library.models.os') as mock_os:
            mock_os.path.exists.return_value = True
            bookmark = BookMark()
            bookmark.url = 'https://google.com'
            bookmark.makeup()
            bookmark.img = 'test'
            self.assertEqual('/storage/test', bookmark.thumbnail)


class ContractTest(BaseTestCase):

    @patch('werkzeug.datastructures.FileStorage')
    @patch('library.contract.resize_img')
    def test_change_thumbnail(self, mock_resize_img, file):
        with patch('library.contract.db') as mock_db:
            b = BookMark()

            file.filename = 'test.png'
            file.save.return_value =True
            mock_resize_img.return_value = True
            # mock_db.session.add.return_value = True
            # mock_db.session.commit.return_value = True

            contract.change_thumbnail(b, file)

            file.save.assert_called_once()
            mock_resize_img.assert_called_once()
            mock_db.session.add.assert_called_once_with(b)

            assert 'test.png' in b.img

    @patch('werkzeug.datastructures.FileStorage')
    @patch('library.contract.resize_img')
    @patch('library.contract.os')
    def test_change_thumbnail_rollback_when_error_occured(self, mock_os, mock_resize_img, file):
        with patch('library.contract.db') as mock_db:
            b = BookMark()

            file.filename = 'test.png'
            file.save.return_value =True
            mock_resize_img.return_value = True

            mock_db.session.add.return_value = True
            mock_db.session.rollback.return_value = True

            mock_db.session.commit.side_effect = IntegrityError

            mock_os.remove.return_value = True

            contract.change_thumbnail(b, file)

            file.save.assert_called_once()
            mock_resize_img.assert_called_once()
            mock_db.session.add.assert_called_once_with(b)
            mock_db.session.rollback.assert_called_once()

            mock_os.remove.assert_called_once()

    def test_register_bookmark_and_tag(self):
        u1 = User()
        b1 = BookMark(url='google.com')
        t1 = Tag(tag='tag1')
        t2 = Tag(tag='tag2')

        contract.register_bookmark_and_tag(u1, b1, t1, t2)
        self.assertEqual(b1, u1.bookmarks[0])
        self.assertEqual(2, len(u1.bookmarks[0].tags))

    def test_register_bookmark_and_tag_rollback_on_error(self):
        with patch('library.contract.db', wraps=db) as mock_db:

          #  mock_db.session.rollback.return_value = None

            mock_db.session.commit.side_effect = IntegrityError

            u1 = User()
            b1 = BookMark(url='google.com')
            t = Tag(tag='tag2')

            t2 = Tag()

            contract.register_bookmark_and_tag(u1, b1, t, t2)
            mock_db.session.rollback.assert_called_once()

            self.assertIsNone(u1.bookmarks[0].id, u1.bookmarks[0].id)
            self.assertEqual(0, Tag.query.count())
            self.assertEqual(0, BookMark.query.count())

