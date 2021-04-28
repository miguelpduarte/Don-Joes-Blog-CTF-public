import requests
from sha256 import sha256
import os
import binascii
import struct

url = "http://don-joes-blog.herokuapp.com/m4st3rfully_h1dd3n"
form = "username=supreme_user&password=ezpz_passw0rd%21"
m2 = b"=a;username=admin;secret=2ae3a0f2ef89bf388e7cdc7f5fc9f1b60e5542d0a6c2f6f1cf88190d0ab2b711;role=1;"

for length in range(8, 15):

    # Obtain data and signature
    req = requests.post(f"{url}/login", data=form, headers={"Content-Type": "application/x-www-form-urlencoded"}, allow_redirects=False)
    if not req.cookies:
        print("No cookies")
        break

    cookie = req.cookies.get('auth')
    data, sig = cookie.split('.')

    m1 = binascii.a2b_base64(data)
    h1 = binascii.a2b_base64(sig)

    # Calculate new signature
    state = []
    for x in range(0, len(h1), 4):
        v = (h1[x] << 24) + (h1[x + 1] << 16) + (h1[x + 2] << 8) + (h1[x + 3])
        state.append(v)

    s = sha256(m=m2, s=state, l=64*(1+(len(m1)+length)//64)) 
    h2 = s.hexdigest()

    # Prepare payload: M1 | Padding | M2
    padding = b'\x80' + b'\0' * (64 - (length + len(m1) + 1 + 8) % 64) + struct.pack('!Q',(len(m1) + length)*8)
    
    ndata = binascii.b2a_base64(m1 + padding + m2).strip().decode('latin')
    nsig  = binascii.b2a_base64(h2).strip().decode('latin')

    cookie = f"auth={ndata}.{nsig}"
    
    # Try cookie
    req = requests.get(f"{url}/admin", headers={'Cookie': cookie})
    
    if 'flag' in req.text:
        print("len: ", length)
        print(req.text)
        break

