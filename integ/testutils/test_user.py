import flask.sessions
import hashlib
from itsdangerous import URLSafeTimedSerializer
import random
import requests
import string
import time


class TestUser(object):

    def __init__(self):
        self.id = None
        self.session = None
        self.session_data = None
        self.password = 'test_password'

        # TODO: move to <something>+<randomization>@gmail.com so that
        # registration emails actually go somewhere we control.
        now = int(time.time())
        salt = ''.join(random.choice(string.ascii_letters) for _ in range(2))
        self.email = ''.join(('test+', salt, '_', str(now), '@example.com'))

        self._create_user()

    def _create_user(self):
        self.session = requests.Session()
        r = self.session.post('http://localhost:5000/login',
                              data={'email': self.email,
                                    'password': self.password})
        r.raise_for_status()

        self.session_data = SessionData(r)
        self.id = self.session_data['id']


class SessionData(dict):
    """Understands flask session data, returning the session dictionary

    Adapted from:
    https://github.com/mitsuhiko/flask/blob/84a12afd4dff0c58aceb34c7fc93e3eedbe5005f/flask/sessions.py#L315-L317
    """

    def __init__(self, request):
        self.cookie = request.cookies['session']

        json_serializer = flask.sessions.TaggedJSONSerializer()
        signer_args = {'key_derivation': 'hmac', 'digest_method': hashlib.sha1}
        s = URLSafeTimedSerializer('devo', salt='cookie-session',
                                   serializer=json_serializer,
                                   signer_kwargs=signer_args)

        for key, val in s.loads(self.cookie).items():
            self[key] = val
