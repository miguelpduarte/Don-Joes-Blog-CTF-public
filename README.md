# Don Joe's Blog (Web/Crypto)

## Problem statement

Don Joe insists his site is as secure as can be! Can you prove the best web dev of all times wrong?

## Summary (solution)

LFI (which excludes `*flag`) to get `passwd` which has flag #1 there as a comment and credentials to a hidden login page. (e.g. `http://localhost:8000/blogpost?id=../../../../../../../../../../etc/passwd`)

After you have the login page, you get the code as a zip file. The credentials are in a python file (so that we don't have to handle a DB) but the passwords are only stored hashed.
The solution to this is to use hash length extension attack since the hashing algorithm is vulnerable to this to "spoof" the session cookie and make the server think we are admins.

The writeup slides are also available in 0xOPOSEC's meetup page.

`cookie_crafter.py` is my solution, the community solutions were provided by folks in the 0xOPOSEC community.

## How to run

Dockerized, use `docker-compose` or the provided `Dockerfile`.

## Used in

`0xOposec` monthly challenge, April 2021

## Inspired by

Hash length extension inspired by HackTheBox Intense.  
LFI inspired by LFI :grin:.

## Related resources

* [LFI on OWASP](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion)
* [HashPump repo](https://github.com/bwall/HashPump)
