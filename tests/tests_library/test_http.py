import io
from flask_security import current_user, url_for_security
from pathlib import Path
from sqlalchemy import desc
from models import User
from bookMarkLibrary.database import db
from bookMarkLibrary.exceptions import InvalidURLException
from library.models import BookMark, Tag
from tests.base import BaseTestCase
from unittest import mock, skip
from flask import url_for, current_app as app, g
import os
import shutil
import logging
import uuid


class AddTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.client.post(url_for_security('register'),
                         data={'email': 'test@test.com', 'password': 'test123',
                               'password_confirm': 'test123'})

    def test_get_add_page(self):
        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})

            add = self.client.get(url_for('library.urls'))
            assert url_for('library.add_ele').encode() in add.data

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()

    def test_add_bookMark(self):
        with self.client:
            # add bookmark with out tag
            data = {'url': 'google.com'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)

            # use og:img as thumbnail
            data = {'url': 'http://ogp.me/'}
            res = self.client.post(url_for('library.add_ele'), data=data)

            og_bookmark = BookMark.query.filter_by(_url='http://www.ogp.me').order_by(desc(BookMark.id)).first()
            self.assertIsNotNone(og_bookmark)
            self.assertEqual('http://www.ogp.me/logo.png', og_bookmark.img)

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'ogp.me' in content
            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tag(self):
        with self.client:
            data = {'url': 'google.com', 'tags': '#new_tag'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

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

    def test_add_bookmark_with_new_tags(self):
        with self.client:
            data = {'url': 'google.com', 'tags': '#new_tag1#new_tag2'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(2, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(2, len(tags))

            for tag in bookmark.tags:
                assert tag in tags

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert 'new_tag1' in content
            assert 'new_tag2' in content
            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_existing_tag(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            db.session.add(t1)
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(1, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(1, len(tags))
            self.assertEquals(tags[0], bookmark.tags[0])

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_existing_tags(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
            db.session.add_all([
                t1, t2
            ])
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(2, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(2, len(tags))
            self.assertEquals(tags[0], bookmark.tags[0])

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert t2.tag in content

            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tags_and_existing_tags(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
            db.session.add_all([
                t1, t2
            ])
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag + '#new1#new2'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(4, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(4, len(tags))

            for tag in bookmark.tags:
                assert tag in tags

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert t2.tag in content
            assert 'new1' in content
            assert 'new2' in content

            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tag_and_existing_tags(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
            db.session.add_all([
                t1, t2
            ])
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag + '#new1'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(3, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(3, len(tags))

            for tag in bookmark.tags:
                assert tag in tags

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert t2.tag in content
            assert 'new1' in content

            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tag_and_existing_tag(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            db.session.add(t1)
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag + '#new2'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()
            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(2, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(2, len(tags))

            for tag in bookmark.tags:
                assert tag in tags

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert 'new2' in content

            assert 'Google' in content

            self.assert_template_used('library/urls.html')

    def test_add_bookmark_with_new_tags_and_existing_tag(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            db.session.add(t1)
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag + '#new1#new2'}
            res = self.client.post(url_for('library.add_ele'), data=data)
            bookmark = BookMark.query.first()
            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEquals(3, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEquals(3, len(tags))

            for tag in bookmark.tags:
                assert tag in tags

            self.assertEquals(bookmark, current_user.bookmarks[0])

            result = self.client.get(url_for('library.urls'))

            content = result.data.decode('utf-8')
            assert t1.tag in content
            assert 'new1' in content
            assert 'new2' in content

            assert 'Google' in content

            self.assert_template_used('library/urls.html')

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

            data = {'url': 'yahoo.invalid'}
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

    def test_search_thumbnail_by_tag(self):
        from bookMarkLibrary.database import db
        user = User.query.first()
        b1 = BookMark(url='http://localhost', name='test_thumbnail')
        b2 = BookMark(url='http://localhost2', name='test_thumbnail2')
        tag = Tag(tag='test_tag')

        b1.tags.append(tag)
        b2.tags.append(tag)

        user.bookmarks.extend([b1, b2])

        db.session.add_all([user, tag])
        db.session.commit()

        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            result = self.client.get(url_for('library.urls',  tag='test_tag'))

            content = result.data.decode('utf-8')
            assert 'test_tag' in content
            assert 'test_thumbnail' in content
            assert 'test_thumbnail2' in content

            self.assert_template_used('library/urls.html')

    def test_search_thumbnail_by_tag_not_exists(self):
        from bookMarkLibrary.database import db
        user = User.query.first()
        b1 = BookMark(url='http://localhost', name='test_thumbnail')
        b2 = BookMark(url='http://localhost2', name='test_thumbnail2')
        tag = Tag(tag='test_tag')
        b1.tags.append(tag)
        b2.tags.append(tag)

        user.bookmarks.extend([b1, b2])
        db.session.commit()

        with self.client:
            self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            result = self.client.get(url_for('library.urls', tag='null'))

            content = result.data.decode('utf-8')
            assert 'null' not in content
            assert 'test_thumbnail' not in content

            self.assert_template_used('library/urls.html')

