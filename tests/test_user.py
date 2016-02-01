import json
import unittest
from unittest.mock import patch

from emoji.user.user import User
from emoji.user.user import UserId


class UserTest(unittest.TestCase):

    @patch('time.time')
    @patch('uuid.uuid4')
    @patch('werkzeug.security.generate_password_hash')
    def test_create(self, generate_password_hash_func, uuid_func, time_func):
        generate_password_hash_func.return_value = 'user_pass_hash'
        uuid_func.return_value = 'uuid'
        time_func.return_value = 123.456

        user = User.create('user_email', 'user_password')

        self.assertEqual('id.usr.123.uuid', str(user.id))
        self.assertEqual('user_email', user.email)
        self.assertEqual('user_pass_hash', user.pass_hash)

    @patch('werkzeug.security.check_password_hash')
    def test_check_password(self, check_password_hash_func):
        user = User(UserId('user_id'), 'user_email', 'user_hash')

        check_password_hash_func.return_value = True
        self.assertTrue(user.check_password('user_password'))

        check_password_hash_func.return_value = False
        self.assertFalse(user.check_password('user_password'))

    def test_to_json(self):
        user = User(UserId('user_id'), 'user_email', 'user_hash')
        js = json.loads(user.to_json())

        self.assertEqual('user_id', js['id'])
        self.assertEqual('user_email', js['email'])
        self.assertEqual('user_hash', js['pass_hash'])

    def test_from_json(self):
        js = """{
        "id": "user_id",
        "email": "user_email",
        "pass_hash": "user_hash"
        }"""
        user = User.from_json(js)

        self.assertEqual(UserId('user_id'), user.id)
        self.assertEqual('user_email', user.email)
        self.assertEqual('user_hash', user.pass_hash)
