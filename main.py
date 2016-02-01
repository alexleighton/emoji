from flask import Flask, jsonify, request, Response, session
from functools import wraps
import redis

from emoji.user.account_service import AccountService
from emoji.user.user import User

app = Flask('emoji')

redis = redis.StrictRedis(host='localhost', port=6379, db=0)
account_service = AccountService(redis)


@app.route('/login', methods=['POST'])
def login():
    email_address = request.form['email']
    password = request.form['password']

    user = account_service.load(email_address)
    if user is not None:
        if not user.check_password(password):
            return fail_authorization()
    else:
        user = create_user(email_address, password)

    session['id'] = str(user.id)
    return jsonify(id=str(user.id))


def fail_authorization():
    return Response('{"error": "unauthorized"}', 401)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'id' not in session:
            return fail_authorization()
        return f(*args, **kwargs)
    return decorated


def create_user(email_address, password):
    user = User.create(email_address, password)
    account_service.store(user)
    return user


if __name__ == '__main__':
    app.secret_key = 'devo'
    app.run(debug=True)
