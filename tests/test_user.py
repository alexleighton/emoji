import json
import unittest

from emoji.user.user import User
from emoji.user.user import UserId

class UserTest(unittest.TestCase):

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
