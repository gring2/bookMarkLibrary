import os
import shutil
import tempfile
import json
from tests.base import BaseTestCase


class JsonHandlerTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.json')
        test_content = {'thumbnails': [{'url':'http://test.com', 'img': 'test.com.png'}]}

        # Category
        # root: {name:root, id:0, sub: [01, 02]}
        # Movie: {name: Movie, id: 01, sub: [13, ]}  Docs: {name: Docs, id: 02 }
        #   |
        # Hero: {name: Hero, id: 13, sub: [134, 135, 136}
        #   |
        # SnapShot
        # Iron-man1{'url':http://ironman1.com', img: 'ironman1.png', id: 134}
        # Iron-man2{'url':http://ironman1.com', img: 'ironman1.png', id: 135}
        # Iron-man3{'url':http://ironman1.com', img: 'ironman1.png', id: 136}

        with open(self.test_file, "wt") as file:
            json.dump(test_content, file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)


