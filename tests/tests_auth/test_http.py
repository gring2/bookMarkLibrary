from bookMarkLibrary.database import db
from models import User
from tests.base import BaseTestCase
from flask_security import login_user, current_user, url_for_security


class AuthTest(BaseTestCase):
    def test_register(self):
        res = self.client.post(url_for_security('register'), data={'email': 'test@test.com', 'password': 'test123', 'password_confirm': 'test123'})
        user = User.query.first()
        self.assertEqual('test@test.com', user.email, 'email  equals')
        login_user(user)

        self.assertEqual(current_user, user, current_user.id)
        self.assertEqual(current_user.email, user.email, current_user.email)
        db.drop_all(bind=None)

    def test_login(self):
        zero = User.query.count()
        self.assertEqual(0, zero)
        self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
        self.assertTrue(current_user.is_anonymous)

        self.client.post(url_for_security('register'), data={'email': 'test@test.com', 'password': 'test123',
                                                             'password_confirm': 'test123'})
        cnt = User.query.count()
        self.assertEqual(1, cnt)

        self.client.get(url_for_security('logout'))

        with self.client:
            it = self.client.post(url_for_security('login'), data={'email': 'test@test.com', 'password': 'test123'})
            t = current_user
            self.assertIsNotNone(t)
            self.assertEqual('test@test.com', t.email)

    def test_login_page(self):
        with self.client:
            res = self.client.get(url_for_security('login'),)

            self.assert_template_used('security/login_user.html')

    def test_register_page(self):
        with self.client:
            res = self.client.get(url_for_security('register'),)

            self.assert_template_used('security/register_user.html')

    def tearDown(self):
        super().tearDown()
