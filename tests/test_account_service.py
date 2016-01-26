import unittest
import unittest.mock

from emoji.user.user import User
from emoji.user.user import UserId
from emoji.user.account_service import AccountService

class AccountServiceTest(unittest.TestCase):

    def setUp(self):
        self.redis = unittest.mock.Mock()
        self.service = AccountService(self.redis)

        self.test_user = User(UserId('stored_id'), 'stored_email', 'stored_hash')


    def test_load_by_id(self):
        self.redis.get.return_value = self.test_user.to_json()

        user = self.service.load(UserId('user_id'))

        self.assertEqual(UserId('stored_id'), user.id)
        self.assertEqual('stored_email', user.email)
        self.assertEqual('stored_hash', user.pass_hash)

        self.redis.get.assert_called_with('user|by_id|user_id')


    def test_load_by_email(self):
        self.redis.get.return_value = self.test_user.to_json()

        user = self.service.load('user_email')

        self.assertEqual(UserId('stored_id'), user.id)
        self.assertEqual('stored_email', user.email)
        self.assertEqual('stored_hash', user.pass_hash)

        self.redis.get.assert_called_with('user|by_email|user_email')


    def test_store(self):
        pipeline_mock = self.redis.pipeline()
        pipeline_mock.set.return_value = pipeline_mock

        user = User('user_id', 'user_email', 'user_hash')
        self.service.store(user)

        pipeline_mock.set.assert_any_call('user|by_id|user_id', user.to_json())
        pipeline_mock.set.assert_any_call('user|by_email|user_email', user.to_json())
        pipeline_mock.execute.assert_any_call()
