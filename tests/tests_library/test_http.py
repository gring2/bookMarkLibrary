import io
from flask_security import url_for_security
from pathlib import Path
from sqlalchemy import desc
from models import User
from bookMarkLibrary.database import db
from bookMarkLibrary.exceptions import InvalidURLException
from library.models import BookMark, Tag
from tests.base import BaseTestCase
from tests import api_utils
from flask import url_for, current_app as app, g
import os
import shutil
import uuid


class AddTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        login = api_utils.post(url_for_security('register'),
                               data={'email': 'test@test.com', 'password': 'test123',
                                     'password_confirm': 'test123'})

        user = api_utils.loads(login.data)['response']['user']
        self.current_user = User.query.get(user['id'])
        self.token = user['authentication_token']

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        db.session.close()
        super().tearDown()

    def test_add_bookMark(self):
        # add bookmark with out tag
        data = {'url': 'google.com'}
        res = api_utils.post(url_for('library.add_ele'), data=data,
                             headers={'Authentication-Token': self.token}
                             )

        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)

        # use og:img as thumbnail
        data = {'url': 'http://ogp.me/'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
        self.assertStatus(res, 204)

        og_bookmark = BookMark.query.filter_by(_url='http://www.ogp.me').order_by(desc(BookMark.id)).first()
        self.assertIsNotNone(og_bookmark)
        self.assertEqual('http://www.ogp.me/logo.png', og_bookmark.img)

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = result.data.decode('utf-8')
        assert 'ogp.me' in content
        assert 'Google' in content

        data = api_utils.loads(result.data)
        self.assertEqual(2, len(data))

    def test_add_bookmark_with_new_tag(self):
        data = {'url': 'google.com', 'tags': '#new_tag'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})

        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(1, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(1, len(tags))
        self.assertEqual(tags[0], bookmark.tags[0])

        current_user = User.query.first()
        self.assertEqual(bookmark, current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(1, len(content['tags']))

        assert Tag.query.filter_by(tag='new_tag').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_new_tags(self):
        data = {'url': 'google.com', 'tags': '#new_tag1#new_tag2'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(2, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(2, len(tags))

        for tag in bookmark.tags:
            assert tag in tags

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(2, len(content['tags']))

        assert Tag.query.filter_by(tag='new_tag1').first().as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new_tag2').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_existing_tag(self):
        with self.client:
            t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
            db.session.add(t1)
            db.session.commit()

            data = {'url': 'google.com', 'tags': '#' + t1.tag}
            res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
            bookmark = BookMark.query.first()

            self.assertIsNotNone(bookmark)
            self.assertIsNotNone(bookmark.img)
            self.assertEqual(1, len(bookmark.tags))

            tags = Tag.query.all()
            self.assertEqual(1, len(tags))
            self.assertEqual(tags[0], bookmark.tags[0])

            self.assertEqual(bookmark, self.current_user.bookmarks[0])

            result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

            content = api_utils.loads(result.data)

            assert t1.as_dict() in content['tags']

            self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_existing_tags(self):
        t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
        t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
        db.session.add_all([
            t1, t2
        ])
        db.session.commit()

        data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(2, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(2, len(tags))
        self.assertEqual(tags[0], bookmark.tags[0])

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(2, len(content['tags']))

        assert t1.as_dict() in content['tags']
        assert t2.as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_new_tags_and_existing_tags(self):
        t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
        t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
        db.session.add_all([
            t1, t2
        ])
        db.session.commit()

        data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag + '#new1#new2'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(4, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(4, len(tags))

        for tag in bookmark.tags:
            assert tag in tags

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = result.data.decode('utf-8')

        content = api_utils.loads(result.data)

        self.assertEqual(4, len(content['tags']))

        assert t1.as_dict() in content['tags']
        assert t2.as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new1').first().as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new2').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_new_tag_and_existing_tags(self):
        t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
        t2 = Tag(id=uuid.uuid4().hex, tag='existing_2')
        db.session.add_all([
            t1, t2
        ])
        db.session.commit()

        data = {'url': 'google.com', 'tags': '#' + t1.tag + '#' + t2.tag + '#new1'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})
        bookmark = BookMark.query.first()

        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(3, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(3, len(tags))

        for tag in bookmark.tags:
            assert tag in tags

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(3, len(content['tags']))

        assert t1.as_dict() in content['tags']
        assert t2.as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new1').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_new_tag_and_existing_tag(self):
        t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
        db.session.add(t1)
        db.session.commit()

        data = {'url': 'google.com', 'tags': '#' + t1.tag + '#new2'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})

        bookmark = BookMark.query.first()
        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(2, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(2, len(tags))

        for tag in bookmark.tags:
            assert tag in tags

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(2, len(content['tags']))

        assert t1.as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new2').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_add_bookmark_with_new_tags_and_existing_tag(self):
        t1 = Tag(id=uuid.uuid4().hex, tag='existing_1')
        db.session.add(t1)
        db.session.commit()

        data = {'url': 'google.com', 'tags': '#' + t1.tag + '#new1#new2'}
        res = api_utils.post(url_for('library.add_ele'), data=data, headers={'Authentication-Token': self.token})

        bookmark = BookMark.query.first()
        self.assertIsNotNone(bookmark)
        self.assertIsNotNone(bookmark.img)
        self.assertEqual(3, len(bookmark.tags))

        tags = Tag.query.all()
        self.assertEqual(3, len(tags))

        for tag in bookmark.tags:
            assert tag in tags

        self.assertEqual(bookmark, self.current_user.bookmarks[0])

        result = api_utils.get(url_for('library.urls'), headers={'Authentication-Token': self.token})

        content = api_utils.loads(result.data)

        self.assertEqual(3, len(content['tags']))

        assert t1.as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new1').first().as_dict() in content['tags']
        assert Tag.query.filter_by(tag='new2').first().as_dict() in content['tags']

        self.assertEqual('Google', content['bookmarks'][0]['name'])

    def test_change_thumbnail(self):
        file = (io.BytesIO(b"abcdef"), 'test.jpg')

        api_utils.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'},
                       headers={'Authentication-Token': self.token})

        bookmark = BookMark(url='dummy.url', img='dummy.png')

        past_img = bookmark.img

        self.current_user.bookmarks.append(bookmark)

        db.session.add(self.current_user)
        db.session.commit()

        data = {'img': file, 'id': BookMark.query.first().id}
        res = self.client.patch(url_for('library.change_thumbnail'),
                                data=data, headers={'Authentication-Token': self.token,
                                                    'Content-Type': 'multipart/form-data'
                                                                                       })

        self.assertNotEqual(past_img, bookmark.img)

        path = Path(app.config['STORAGE_PATH'] + '/' + bookmark.img)
        self.assertTrue(path.is_file())
        self.assertStatus(res, 204)

    def test_invalid_url(self):
        api_utils.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'},
                       headers={'Authentication-Token': self.token})

        data = {'url': 'yahoo.invalid'}
        res = api_utils.post(url_for('library.add_ele'), data=data)

        self.assert500(res)
        self.assertRaises(InvalidURLException)

        bookmark_cnt = BookMark.query.count()

        self.assertEqual(0, bookmark_cnt)


class ShowTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

        login = api_utils.post(url_for_security('register'),
                               data={'email': 'test@test.com', 'password': 'test123',
                                     'password_confirm': 'test123'})

        user = api_utils.loads(login.data)['response']['user']
        self.token = user['authentication_token']

    def test_show_thumbnails(self):
        from bookMarkLibrary.database import db
        user = User.query.first()
        b1 = BookMark(url='http://localhost', name='test_thumbnail')
        b2 = BookMark(url='http://localhost2', name='test_thumbnail2')

        user.bookmarks.extend([b1, b2])

        db.session.add_all([user])
        db.session.commit()

        result = api_utils.get(url_for('library.urls'), headers={
            'Authentication-Token': self.token
        })

        content = api_utils.loads(result.data.decode('utf-8'))

        assert 'bookmarks' in content
        assert 'tags' in content
        self.assertEqual([b1.as_dict(), b2.as_dict()], content['bookmarks'])

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

        result = api_utils.get(url_for('library.urls', tag='test_tag'), headers={
            'Authentication-Token': self.token
        })

        content = api_utils.loads(result.data.decode('utf-8'))
        self.assertEqual(1, len(content['tags']))

        self.assertEqual([{'id': tag.id.__str__(), 'tag': tag.tag}], content['tags'])
        self.assertEqual([b1.as_dict(), b2.as_dict()], content['bookmarks'])

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

        result = api_utils.get(url_for('library.urls', tag='null'), headers={
            'Authentication-Token': self.token
        })

        content = api_utils.loads(result.data.decode('utf-8'))
        self.assertEqual(0, len(content['bookmarks']))
        self.assertEqual(1, len(content['tags']))
