import json

import emoji.id

class User(object):

    def __init__(self, id, email, pass_hash):
        self.id = id
        self.email = email
        self.pass_hash = pass_hash

    def to_json(self):
        return json.dumps({
            'id': str(self.id),
            'email': self.email,
            'pass_hash': self.pass_hash,
        })

    @staticmethod
    def from_json(json_blob):
        u = json.loads(json_blob)
        return User(id=UserId(u['id']),
                    email=u['email'],
                    pass_hash=u['pass_hash'])


class UserId(emoji.id.Id):

    @staticmethod
    def generate():
        return UserId(Id.generate_str('usr'))
