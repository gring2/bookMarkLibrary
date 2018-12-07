import os
import bookMarkLibrary
import unittest

app = bookMarkLibrary.create_app()


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = bookMarkLibrary.create_app({
            'WTF_CSRF_ENABLED': False
        })

        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()


