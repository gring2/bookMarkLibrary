from tests.base import BaseTestCase
from unittest import  mock
from flask import url_for, current_app as app
import os
import shutil
from utils.json_handler import fetch_data_obj
from library.models import SnapShot


class AddTestCase(BaseTestCase):

    def test_get_add_page(self):

        add = self.client.get(url_for('library.add'))
        assert b'add url' in add.data

    def test_make_library_file(self,):
        # mocking selenium dependency
        with mock.patch('utils.snapshot_handler.webdriver') as driver:
            # stubbing functions with dummy returns
            driver.return_value.get.return_value = 'testing'
            driver.return_value.save_screenshot.return_value = 'save_screenshot'
            json_data_defulat = fetch_data_obj(app.config['STORAGE_PATH'] + "/test.json")
            assert 'thumbnails' in json_data_defulat

            self.client.post(url_for('library.add'), data={'url': 'http://twitter.com'})
            exists = os.path.exists(app.config['STORAGE_PATH'] + "/test.json")
            assert exists is True

            json_data = fetch_data_obj(app.config['STORAGE_PATH'] + "/test.json")
            assert 'thumbnails' in json_data
            assert 'http://twitter.com' in json_data['thumbnails'][0].url
            self.client.post(url_for('library.add'), data={'url': 'http://google.com'})
            json_data = fetch_data_obj(app.config['STORAGE_PATH'] + "/test.json")

            self.assertIn('http://google.com', json_data['thumbnails'][1].url)
            self.assertIn('google.com', json_data['thumbnails'][1].img)

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()


class ShowTestCase(BaseTestCase):

    def test_show_thumbnails(self):
        # mocking selenium dependency
        with mock.patch('library.view.json_handler.fetch_data_obj', return_value={'thumbnails': [SnapShot(**{'url':'http://test.com', 'img': 'test.com.png'})]}) as json_handler:
            result = self.client.get(url_for('library.urls'))
            content = result.data.decode('utf-8')
            assert 'test.com.png' in content

    def tearDown(self):
        shutil.rmtree(app.config['STORAGE_PATH'])
        os.makedirs(app.config['STORAGE_PATH'])
        super().tearDown()
