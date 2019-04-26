from bookMarkLibrary.database import db
from flask_testing import TestCase
import os
import bookMarkLibrary.app as base_app


app = base_app.create_app(
    {
        'WTF_CSRF_ENABLED': False,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:////' + os.path.join(base_app.ROOT_DIR, '../instance/bookmark_test.sqlite'),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,

    }
)


class BaseTestCase(TestCase):

    def create_app(self):
        self.app = app

        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all(bind=None)
        return app

    def tearDown(self):

        db.drop_all(bind=None)
        super().tearDown()
