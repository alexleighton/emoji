import json

from emoji.user.user import User, UserId

class AccountService(object):

    def __init__(self, redis):
        self.redis = redis

    def load(self, id):
        if isinstance(id, UserId):
            return self.load_by_id(id)
        else:
            return self.load_by_email(id)

    def load_by_id(self, id):
        key = _by_id_index(id)
        return self._load_by_key(key)

    def load_by_email(self, email_address):
        key = _by_email_index(email_address)
        return self._load_by_key(key)

    def _load_by_key(self, key):
        user_json = self.redis.get(key).decode(_UTF8)
        return User.from_json(user_json)

    def store(self, user):
        user_json = user.to_json().encode(_UTF8)

        self.redis.pipeline()                             \
            .set(_by_id_index(user.id), user_json)        \
            .set(_by_email_index(user.email), user_json)  \
            .execute()

_UTF8 = 'utf-8'
_SEP = '|'

def _by_id_index(user_id):
    return _SEP.join( ('user', 'by_id', str(user_id)) )

def _by_email_index(email_address):
    return _SEP.join( ('user', 'by_email', email_address) )
