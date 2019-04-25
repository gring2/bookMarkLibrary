import io
from flask_security import current_user, url_for_security
from pathlib import Path
from sqlalchemy import desc

from bookMarkLibrary.database import db
from library.models import Category, BookMark
from tests.base import BaseTestCase
from unittest import mock, skip
from flask import url_for, current_app as app, g
import os
import shutil
from tests.data_factory import test_library_dict_factory
import logging


class AddTestCase(BaseTestCase):
    def test_logger(self):
        logging.debug('debug')
        logging.error(Exception('error'))
        logging.warning(Exception('critical'))
        logging.critical(Warning('warning'))
        logging.info('info')
        self.assertTrue(True)

    def test_get_add_page(self):
        with self.client:
            res = self.client.post(url_for_security('register'),
                                   data={'email': 'test@test.com', 'password': 'test123',
                                         'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            add = self.client.get(url_for('library.urls'))
            assert url_for('library.add_ele').encode() in add.data


    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()

@skip
class ShowTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_show_thumbnails(self):
        # mocking selenium dependency

        with mock.patch('handlers.category_handler.fetch_sub_category', return_value=test_library_dict_factory()):
            with self.client:
                res = self.client.post(url_for_security('register'),
                                       data={'email': 'test@test.com', 'password': 'test123',
                                             'password_confirm': 'test123'})

                self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
                result = self.client.get(url_for('library.urls'))

                content = result.data.decode('utf-8')
                assert 'div' in content
                self.assert_template_used('library/urls.html')

    def test_add_category(self):
        self.client.post(url_for_security('register'), data={'email': 'test@test.com', 'password': 'test123',
                                                                   'password_confirm': 'test123'})
        self.client.get(url_for_security('logout'))
        with self.client:
            self.client.post(url_for_security('login'), data={'email':'test@test.com', 'password':'test123'})
            self.client.get(url_for('library.urls'))
            c = Category.query.filter_by(user_id=current_user.id).count()
            self.assertEqual(1, c)
            res = self.client.post(url_for('library.add_ele'), data={'kind': '1', 'path': 'category', 'parent_id': '1'})
            c = Category.query.filter_by(user_id=current_user.id).count()

            self.assertEqual(2, c)

    def test_add_bookMark(self):
        with mock.patch('handlers.screenshot_handler.ScreenShotHandler.make_screenshot', return_value='mock_img_name'):

            with self.client:
                res = self.client.post(url_for_security('register'),
                                       data={'email': 'test@test.com', 'password': 'test123',
                                             'password_confirm': 'test123'})

                self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
                add = self.client.get(url_for('library.urls'))

                kind = g.kind
                # add bookmark to root category
                book_mark_kind = kind['book_mark']['code']
                root_category = Category.query.filter_by(user_id=current_user.id).first()
                data = {'kind': book_mark_kind, 'parent_id': root_category.id, 'path': 'google.com'}
                res = self.client.post(url_for('library.add_ele'), data=data)

                bookmark = BookMark.query.filter_by(parent_id=root_category.id).first()
                assert bookmark is not None
                self.assertEqual('mock_img_name', bookmark.img)

                # add sub category to root category
                category_kind = kind['category']['code']
                data = {'kind': category_kind, 'parent_id': root_category.id, 'path': 'subcategory'}
                res = self.client.post(url_for('library.add_ele'), data=data)

                sub_category = Category.query.filter_by(parent_id=root_category.id, user_id=current_user.id).first()
                assert sub_category is not None
                self.assertEqual('subcategory', sub_category.name)

                # add bookmark to sub category
                data = {'kind': book_mark_kind, 'parent_id': sub_category.id, 'path': 'sub bookmark'}
                res = self.client.post(url_for('library.add_ele'), data=data)

                sub_bookmark = BookMark.query.filter_by(parent_id=sub_category.id).first()
                assert sub_bookmark is not None
                self.assertEqual('mock_img_name', sub_bookmark.img)

                #use og:img as thumbnail
                data = {'kind': book_mark_kind, 'parent_id': sub_category.id, 'path': 'http://ogp.me/'}
                res = self.client.post(url_for('library.add_ele'), data=data)

                og_bookmark = BookMark.query.filter_by(parent_id=sub_category.id).order_by(desc(BookMark.id)).first()
                assert og_bookmark is not None
                self.assertEqual('http://ogp.me/logo.png', og_bookmark.img)


    def test_change_thumbnail(self):
        file = (io.BytesIO(b"abcdef"), 'test.jpg')

        with self.client:
            res = self.client.post(url_for_security('register'),
                                   data={'email': 'test@test.com', 'password': 'test123',
                                         'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            add = self.client.get(url_for('library.urls'))
            root_category = Category.query.filter_by(user_id=current_user.id).first()

            bookmark = BookMark(url='dummy.url', img='dummy.png', parent_id=root_category.id)
            db.session.add(bookmark)
            db.session.commit()
            data= {'thumbnail': file, 'id': BookMark.query.first().id}
            self.client.post(url_for('library.change_thumbnail'), data=data)
            path = Path(app.config['STORAGE_PATH'] + '/dummy.png')

            self.assertTrue(path.is_file())

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()

