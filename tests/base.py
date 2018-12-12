import os
from sqlalchemy import MetaData

import bookMarkLibrary
import unittest
from sqlalchemy import create_engine
from flask import current_app

from bookMarkLibrary import db


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = bookMarkLibrary.create_app({
            'WTF_CSRF_ENABLED': False
        })

        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all(bind=None)

    def tearDown(self):
        db.drop_all(bind=None)
        super().tearDown()


