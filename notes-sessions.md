# Flask Sessions

A flask session object is like a cookie that gets back and forth on every request
* we can treat it like a python dictionary
* It's globally available, which is what makes it useful. e.g. when you sign-in into something, your username is usually stored in a session, which persists as you navigate the website
* It's NOT secure
* It's stored on the user's browser
* Makes it hard to track data flows, though. 

### Why it's not secure

**Do not store anything valuable or sensitive in the session cookie.** IRL, using the username is still quite sensitive, so use an internally-generated unique user id instead. 

You can retrieve the session values by decoding it in base64. 
1. Retrieve the encoded session value from the chrome dev console. 
2. Do this in a python terminal:

```
import secrets
import base64

base64.b64decode("eyJVU0VSTkFNRSI6IkJqb3JuIHRoZSBGZWxsLWhhbmRlZCJ9.EaeIuA.V_348FbJ5zeBQggyI3MmsB60EqQ")
>b'{"USERNAME":"Bjorn the Fell-handed"}\x11\xa7\x88\xb8\x05w\xe3\xc1[\'\x9c\xde\x05\x08 \xc8\x8d\xcc\x9a\xc0z\xd0J\x90'
```
