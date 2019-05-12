import io
from flask_security import current_user, url_for_security
from pathlib import Path
from sqlalchemy import desc

from bookMarkLibrary.database import db
from bookMarkLibrary.exceptions import InvalidURLException
from library.models import BookMark
from tests.base import BaseTestCase
from unittest import mock, skip
from flask import url_for, current_app as app, g
import os
import shutil
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


class ShowTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_show_thumbnails(self):
        # mocking selenium dependency
        with self.client:
            res = self.client.post(url_for_security('register'),
                                   data={'email': 'test@test.com', 'password': 'test123', 'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'div' in content
            self.assert_template_used('library/urls.html')

    def test_add_bookMark(self):

        with self.client:
            res = self.client.post(url_for_security('register'),
                                   data={'email': 'test@test.com', 'password': 'test123',
                                         'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            add = self.client.get(url_for('library.urls'))

            kind = g.kind
            # add bookmark with out tag
            data = {'path': 'google.com'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            bookmark = BookMark.query.filter_by(path=data['path']).first()
            assert bookmark is not None
            self.assertIsNotNone(bookmark.img)

            self.fail('add bookmark with new tag')

            self.fail('add bookmark with new tags')

            self.fail('add bookmark with existing tags')

            self.fail('add bookmark with existing tags and new tags')

            # use og:img as thumbnail
            data = {'path': 'http://ogp.me/'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            og_bookmark = BookMark.query.filter_by(path=data['path']).order_by(desc(BookMark.id)).first()
            assert og_bookmark is not None
            self.assertEqual('http://ogp.me/logo.png', og_bookmark.img)

    def test_change_thumbnail(self):
        file = (io.BytesIO(b"abcdef"), 'test.jpg')

        with self.client:
            self.client.post(url_for_security('register'),
                             data={'email': 'test@test.com', 'password': 'test123',
                             'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            self.client.get(url_for('library.urls'))

            bookmark = BookMark(url='dummy.url', img='dummy.png')

            past_img = bookmark.img

            db.session.add(bookmark)
            db.session.commit()

            data = {'thumbnail': file, 'id': BookMark.query.first().id}
            self.client.post(url_for('library.change_thumbnail'), data=data)

            self.assertNotEqual(past_img, bookmark.img)

            path = Path(app.config['STORAGE_PATH'] + '/' + bookmark.img)
            self.assertTrue(path.is_file())

    def test_invalid_url(self):
        with self.client:
            res = self.client.post(url_for_security('register'),
                                   data={'email': 'test@test.com', 'password': 'test123',
                                         'password_confirm': 'test123'})

            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            kind = g.kind
            # add bookmark to root category
            book_mark_kind = kind['book_mark']['code']

            data = {'kind': book_mark_kind, 'parent_id': '1', 'path': 'yahoo.invalid'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            self.assertRedirects(res, url_for('library.urls') + '/1')
            self.assertRaises(InvalidURLException)

            bookmark_cnt = BookMark.query.count()

            self.assertEqual(0, bookmark_cnt)

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()
