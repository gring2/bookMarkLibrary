
from flask import url_for, current_app as app
from flask_migrate import downgrade, Config
from bookMarkLibrary import User, db
from tests.base import BaseTestCase
from flask_security import login_user, current_user, AnonymousUser
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

    def test_login(self):
        zero = User.query.count()
        self.assertEqual(0,zero)
        self.client.post(url_for('auth.login'), data={'email':'test@test.com', 'password':'test123'})
        self.assertTrue(current_user.is_anonymous)
        self.client.post(url_for('auth.register'), data={'email':'test@test.com', 'password':'test123'})

        cnt = User.query.count()
        self.assertEqual(1,cnt)

        self.client.post(url_for('auth.login'), data={'email':'test@test.com', 'password':'test123'})
        self.assertIsNotNone(current_user)

    def tearDown(self):
        super().tearDown()
