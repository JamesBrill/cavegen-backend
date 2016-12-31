import base64
import hashlib

def hash_email(email):
    hash_object = hashlib.md5(email.encode('utf-8'))
    hash_string = hash_object.hexdigest()
    return hash_string[2:]

def username_handler(payload):
    username = hash_email(payload.get('email'))
    if 'email_verified' in payload and not payload['email_verified']:
        username = None
    return username

def decode_secret(secret):
    return base64.b64decode(secret.replace("_", "/").replace("-", "+"))
