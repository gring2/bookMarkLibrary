from tests.base import BaseTestCase
from flask import url_for, current_app as app
import os
import shutil
from library.json_handler import get_data_obj


class AddTestCase(BaseTestCase):

    def test_get_add_page(self):

        add = self.client.get(url_for('library.add'))
        assert b'add url' in add.data

    def test_make_library_file(self):
        self.client.post(url_for('library.add'), data={'url': 'http://twitter.com'})
        exists = os.path.exists(app.config['STORAGE_PATH'] + "/test.json")
        assert exists is True

        json_data = get_data_obj(app.config['STORAGE_PATH'] + "/test.json")
        assert 'url' in json_data
        assert 'http://twitter.com' in json_data['url']
        self.client.post(url_for('library.add'), data={'url': 'http://google.com'})
        json_data = get_data_obj(app.config['STORAGE_PATH'] + "/test.json")

        self.assertIn('http://google.com', json_data['url'])

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()
