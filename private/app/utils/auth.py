from hashlib import sha256

import utils.sessions as sessions
from utils.users_db import users

def hash_password(password):
    """ Hash password with a secure hashing function """
    return sha256(password.encode()).hexdigest()

def _get_user(username, hashed_pw):
    """ Returns a user object given an username and hashed password using the internal 'DB', if one such user exists """
    for user in users:
        if user['username'] == username and user['password'] == hashed_pw:
            return user
    return None

def try_login(form):
    """ Try to login with the submitted user info """
    if not form:
        return None
    username = form["username"]
    password = hash_password(form["password"])
    result = _get_user(username, password)
    if result:
        return {"username": username, "secret":password}
    return None


def get_session(request):
    """ Get user session and parse it """
    if not request.cookies:
        return 
    if "auth" not in request.cookies:
        return
    cookie = request.cookies.get("auth")
    try:
        info = sessions.parse_session(cookie)
    except sessions.SignatureNotValid:
        return {"status": -1, "msg": "Invalid signature"}
    return info

def get_user_from_session(session):
    if "username" in session and "secret" in session:
        username = session["username"].decode()
        password = session["secret"].decode()
        return _get_user(username, password)

def is_admin(request):
    session = get_session(request)
    # print(session)
    if not session:
        return None
    user = get_user_from_session(session)
    print('authdbg', session, user)

    return user and user['role'] == 1
