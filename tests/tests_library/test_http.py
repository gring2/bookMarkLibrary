
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

    def test_add_category(self):
        self.fail('not implemented')

    def test_add_bookMark(self):
        self.fail('not implemented')

    def test_change_thumbnail(self):
        self.fail('not implemented')

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()
