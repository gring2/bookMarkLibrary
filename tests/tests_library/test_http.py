
from flask_security import current_user, url_for_security

from tests.base import BaseTestCase
from unittest import  mock
from flask import url_for, current_app as app
import os
import shutil

from tests.data_factory import test_library_dict_factory
from handlers.category_handler import fetch_bookmark_elem


class AddTestCase(BaseTestCase):

    def test_get_add_page(self):

        add = self.client.get(url_for('library.input_url'))
        assert b'add url' in add.data

    def test_make_library_file(self,):
        # mocking selenium dependency
        with mock.patch('handlers.snapshot_handler.webdriver') as driver:
            # stubbing functions with dummy returns
            driver.return_value.get.return_value = 'testing'
            driver.return_value.save_screenshot.return_value = 'save_screenshot'
            json_data_defulat = fetch_bookmark_elem(app.config['STORAGE_PATH'] + "/test.json")
            assert 'thumbnails' in json_data_defulat

            self.client.post(url_for('library.input_url'), data={'url': 'http://twitter.com', 'parent': '0'})
            exists = os.path.exists(app.config['STORAGE_PATH'] + "/test.json")
            assert exists is True

            json_data = fetch_bookmark_elem(app.config['STORAGE_PATH'] + "/test.json")
            assert 'thumbnails' in json_data
            assert 'http://twitter.com' in json_data['thumbnails'].sub[0].url
            self.client.post(url_for('library.input_url'), data={'url': 'http://google.com', 'parent': '0'})
            json_data = fetch_bookmark_elem(app.config['STORAGE_PATH'] + "/test.json")

            self.assertIn('http://google.com', json_data['thumbnails'].sub[1].url)
            self.assertIn('google.com', json_data['thumbnails'].sub[1].img)

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()


class ShowTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def test_show_thumbnails(self):
        # mocking selenium dependency

        with mock.patch('handlers.category_handler.fetch_bookmark_elem', return_value=test_library_dict_factory()):
            with self.client:
                res = self.client.post(url_for_security('register'),
                                       data={'email': 'test@test.com', 'password': 'test123',
                                             'password_confirm': 'test123'})

                self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
                result = self.client.get(url_for('library.urls'))

                content = result.data.decode('utf-8')
                assert 'div' in content
                self.assert_template_used('library/urls.html')
                #assert 'test.com.png' in content

    def test_add_category_page(self):
        self.client.post(url_for('auth.register'), data={'email':'test@test.com', 'password':'test123'})
        self.client.post(url_for('auth.login'), data={'email':'test@test.com', 'password':'test123'})

        self.assertTrue(current_user.email == 'test@test.com')
        result = self.client.get(url_for('library.input_category'))
        content = result.data.decode('utf-8')
        assert 'root' in content
        with mock.patch('library.view.json_handler.fetch_data_obj', return_value=test_library_dict_factory()):
            result = self.client.get(url_for('library.input_category'))
            content = result.data.decode('utf-8')
            assert 'root' in content
            assert 'Movie1' in content
            assert 'Movie2' in content

            assert 'root1' in content

    def test_use_same_sequenced_id(self):
        self.client.post(url_for('auth.login'), data={'email': 'test@test.com', 'password': 'test123'})
        self.client.post(url_for('auth.register'), data={'email': 'test@test.com', 'password': 'test123'})

        # create sub-directories
        # assert they use sequential_id

        # create thumbnails
        # assert they share sequential_id with directories above
        self.fail('snap shot and directory use same sequence')

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()
