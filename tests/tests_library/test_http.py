import io
from flask_security import current_user, url_for_security
from pathlib import Path
from sqlalchemy import desc

from bookMarkLibrary.database import db
from bookMarkLibrary.exceptions import InvalidURLException
from library.models import BookMark, Tag
from tests.base import BaseTestCase
from unittest import mock, skip
from flask import url_for, current_app as app, g
import os
import shutil
import logging


class AddTestCase(BaseTestCase):
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

        self.client.post(url_for_security('register'),
                           data={'email': 'test@test.com', 'password': 'test123',
                                 'password_confirm': 'test123'})

    def test_show_thumbnails(self):
        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'main' in content
            self.assert_template_used('library/urls.html')

    def test_add_bookMark(self):
        with self.client:
            # add bookmark with out tag
            data = {'url': 'google.com'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            bookmark = BookMark.query.filter_by(_url=data['path']).first()
            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)

            # use og:img as thumbnail
            data = {'path': 'http://ogp.me/'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            og_bookmark = BookMark.query.filter_by(path=data['path']).order_by(desc(BookMark.id)).first()
            self.assertIsNotNone(og_bookmark)
            self.assertEqual('http://ogp.me/logo.png', og_bookmark.img)

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'opg.me' in content
            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tag(self):
        with self.client:
            data = {'url': 'google.com', 'tags': ['new_tag']}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.filter_by(_url=data['url']).first()
            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(1, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(1, len(tags))
            self.assertEquals(tags[0], bookmark.tags[0])

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'new_tag' in content
            assert 'Google' in content

            self.assert_template_used('library/urls.html')

        self.fail('add bookmark with new tag')

    def test_add_bookmark_with_new_tags(self):

        self.fail('add bookmark with new tags')

    def test_add_bookmark_with_existing_tag(self):
        self.fail('add bookmark with existing tag')

    def test_add_bookmark_with_existing_tags(self):

        self.fail('add bookmark with existing tags')

    def test_add_bookmark_with_new_tags_and_existing_tags(self):
        self.fail('add bookmark with existing tags and new tags')

    def test_add_bookmark_with_new_tag_and_existing_tags(self):
        self.fail('add bookmark with existing tags and new tag')

    def test_add_bookmark_with_new_tag_and_existing_tag(self):
        self.fail('add bookmark with existing tag and new tag')

    def test_add_bookmark_with_new_tags_and_existing_tag(self):
        self.fail('add bookmark with existing tag and new tags')

    def test_change_thumbnail(self):
        file = (io.BytesIO(b"abcdef"), 'test.jpg')

        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            bookmark = BookMark(url='dummy.url', img='dummy.png')

            past_img = bookmark.img

            current_user.bookmarks.append(bookmark)

            db.session.add(current_user)
            db.session.commit()

            data = {'thumbnail': file, 'id': BookMark.query.first().id}
            self.client.post(url_for('library.change_thumbnail'), data=data)

            self.assertNotEqual(past_img, bookmark.img)

            path = Path(app.config['STORAGE_PATH'] + '/' + bookmark.img)
            self.assertTrue(path.is_file())

    def test_invalid_url(self):
        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            data = {'path': 'yahoo.invalid'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            self.assertRedirects(res, url_for('library.urls'))
            self.assertRaises(InvalidURLException)

            bookmark_cnt = BookMark.query.count()

            self.assertEqual(0, bookmark_cnt)

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        db.session.close()
        super().tearDown()
