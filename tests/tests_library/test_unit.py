import os
import shutil
import tempfile
import json
from flask import url_for
from tests.base import BaseTestCase
from library.models import Category, SnapShot
from tests.data_factory import test_library_dict_factory
from utils.json_handler import JSONEncoder,fetch_data_obj


class JsonHandlerTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.json')
        self.test_data = test_library_dict_factory()
        # Category
        # root: {name:root, id:0, sub: [root1, root2]}
        # Movie: {name: Movie, id: r1, sub: [Movie1, Movie2 ]} , SnapShot(**{'id': 'root2', 'url': 'http://test.com', 'img': 'test.com.png'})
        #   |
        # Hero: {name: Hero, id: Movie1, sub: [0111, 0112, 0113},  Documentary: {name: Documentary, id: Movie1 }
        #   |
        # SnapShot
        # Iron-man1{'url':http://ironman1.com', img: 'ironman1.png', id: Hero1}
        # Iron-man2{'url':http://ironman1.com', img: 'ironman1.png', id: Hero2}
        # Iron-man3{'url':http://ironman1.com', img: 'ironman1.png', id: Hero3}

        with open(self.test_file, "wt") as file:
            json.dump(self.test_data, file, cls=JSONEncoder)

    def test_fetch_object_from_json(self):
        data = fetch_data_obj(self.test_file)
        self.assertEqual(json.dumps(data, cls=JSONEncoder), json.dumps(self.test_data, cls=JSONEncoder), self.test_data)

    def tearDown(self):
        shutil.rmtree(self.test_dir)


class LibraryTest(BaseTestCase):
    def test_use_same_sequenced_id(self):
        self.client.post(url_for('auth.login'), data={'email':'test@test.com', 'password':'test123'})
        self.client.post(url_for('auth.register'), data={'email':'test@test.com', 'password':'test123'})

        # create sub-directories
        # assert they use sequential_id

        #create thumbnails 
        #assert they share sequential_id with directories above
        self.fail('snap shot and directory use same sequence')
