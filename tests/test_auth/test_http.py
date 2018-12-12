
from flask import url_for, current_app as app
from flask_migrate import downgrade, Config
from bookMarkLibrary import User, db
from tests.base import BaseTestCase


class AuthTest(BaseTestCase):
    def test_register(self):
        self.client.post(url_for('auth.register'), data={'email':'test@test.com', 'password':'test123'})
        user=User.query.first()
        self.assertEqual('test@test.com', user.email, 'email  equals')

        db.drop_all(bind=None)

    def test_login(self):
        self.fail('login user')

    def tearDown(self):
        super().tearDown()
