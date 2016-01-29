import requests
import unittest

from testutils.test_user import TestUser, SessionData

class LoginTest(unittest.TestCase):

    def test_user_creation(self):
        user = TestUser()
        self.assertTrue('id.usr' in user.id)


    def test_user_login_success(self):
        user = TestUser()

        r = requests.post('http://localhost:5000/login',
                          data = { 'email': user.email, 'password': user.password })
        session = SessionData(r)

        self.assertEqual(requests.codes.ok, r.status_code)
        self.assertTrue('id.usr' in session['id'])


    def test_user_login_failure(self):
        user = TestUser()

        r = requests.post('http://localhost:5000/login',
                          data = { 'password': 'wrong_password', 'email': user.email })

        self.assertEqual(requests.codes.unauthorized, r.status_code)
