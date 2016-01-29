import fakeredis
import unittest

from emoji.user.user import User, UserId
from emoji.user.account_service import AccountService


class AccountServiceDBTest(unittest.TestCase):

    def setUp(self):
        self.redis = fakeredis.FakeStrictRedis()
        self.service = AccountService(self.redis)

    def test_store_and_load(self):
        user = User(UserId('stored_id'), 'stored_email', 'stored_hash')

        self.service.store(user)

        user_by_email = self.service.load('stored_email')
        self.assertEqual('stored_id', str(user_by_email.id))
        self.assertEqual('stored_email', user_by_email.email)
        self.assertEqual('stored_hash', user_by_email.pass_hash)

        user_by_id = self.service.load(UserId('stored_id'))
        self.assertEqual('stored_id', str(user_by_email.id))
        self.assertEqual('stored_email', user_by_email.email)
        self.assertEqual('stored_hash', user_by_email.pass_hash)

    def test_load_missing(self):
        user = self.service.load('missing_email')
        self.assertIsNone(user)
