from hashlib import sha256
from base64 import b64decode, b64encode
from random import randrange
import os

SECRET = os.urandom(randrange(8, 15))


class SignatureNotValid(Exception):
    pass


def sign_msg(msg):
    """ Sign the given message with our internal and random secret key """
    return sha256(SECRET + msg).digest()


def verify_signature(data, sig):
    """ Verify that a given signature is valid or not """
    return sign_msg(data) == sig


def parse_session(cookie):
    """ Parse the given cookie and return a dictionary with the parsed data
        @cookie: "key1=value1;key2=value2"

        return {"key":"value","another_key":"another_value"}
    """
    b64_data, b64_sig = cookie.split('.')
    data = b64decode(b64_data)
    sig = b64decode(b64_sig)
    if not verify_signature(data, sig):
        raise SignatureNotValid
    info = {}
    for group in data.split(b';'):
        try:
            if not group:
                continue
            key, val = group.split(b'=')
            info[key.decode()] = val
        except Exception:
            continue
    return info


def create_session(data):
    """ Create a session based on data dictionary
        @data: {"key":"value","another_key":"another_value"}

        return "key=value;another_key=another_value;"
    """
    session = ""
    for k, v in data.items():
        session += f"{k}={v};"
    return session.encode()


def create_cookie(session):
    cookie_sig = sign_msg(session)
    return b64encode(session) + b'.' + b64encode(cookie_sig)
