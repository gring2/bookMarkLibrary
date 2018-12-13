
from flask import url_for, current_app as app
from flask_migrate import downgrade, Config
from bookMarkLibrary import User, db
from tests.base import BaseTestCase
from flask_security import login_user, current_user
import unittest

class AuthTest(BaseTestCase):
    def test_register(self):
        print("Test Register")
        self.client.post(url_for('auth.register'), data={'email':'test@test.com', 'password':'test123'})
        user=User.query.first()
        self.assertEqual('test@test.com', user.email, 'email  equals')
        login_user(user)

        self.assertEqual(current_user, user, current_user.id)
        self.assertEqual(current_user.email, user.email, current_user.email)        
        db.drop_all(bind=None)
    @unittest.skip
    def test_login(self):
        self.fail('login user')

    def tearDown(self):
        super().tearDown()
