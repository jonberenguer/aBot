from sys import argv
import base64
import os
import string
import random
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


"""
install pacakage python3-cryptography 

prgm 0|1 password salt message|token


password = b"password"
salt = os.urandom(16)
"""


def decrypt(password, salt, token):
    bsalt = bytes(salt, 'utf-8')
    bpasword  = bytes(password, 'utf-8')
    btoken  = bytes(token, 'utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bsalt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(bpasword))

    f = Fernet(key)
    #print(f.decrypt(token))
    return f.decrypt(btoken)


def encrypt(password, salt, message):
    bsalt = bytes(salt, 'utf-8')
    bpasword  = bytes(password, 'utf-8')
    bmessage  = bytes(message, 'utf-8')

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=bsalt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(bpasword))

    f = Fernet(key)
    #token = f.encrypt(b"Secret message!")
    #print(token)
    return f.encrypt(bmessage)


def random_return(stringLength=16, punctuation=False):
    if punctuation:
        string_range = string.ascii_letters + string.digits + string.punctuation 
    else: 
        string_range = string.ascii_letters + string.digits

    return ''.join(random.choice(string_range) for i in range(stringLength))


def app():
    try:
        engine = argv[1]
        password  = argv[2]
        salt  = argv[3]
        content = argv[4]

        if engine == '0':
            print(encrypt(password, salt, content).decode('utf-8'))
        elif engine == '1':
            print(decrypt(password, salt, content).decode('utf-8'))
        else:
            print(random_return())
    except:
        print(random_return())
    finally:
        engine = None
        password  = None
        salt  = None
        content = None

        del engine
        del password
        del salt
        del content



if __name__ == "__main__":
    app()








"""
pip3 install pyinstaller

pyinstaller cryptor.py --oneline


./cryptor 0 password 'neJbmkD8qMvNBVVa' 'this is a message'

./cryptor 1 password 'neJbmkD8qMvNBVVa' 'gAAAAABd06-Ltg0hMkGzWWT-W3qH1XfSqgZizLg-o5hHy4368tQ_D6Z1hNEMdP6C8brmFua8jTOyOSUrjoGkasGysSeWdOErhBQfdW_Lp_xKc2p-IUQD0S0='


./cryptor 1 password 'neJbmkD8qMvNBVVa' 'gAAAAABd07DhWKu_K8BZqLMT09jk6l1W_f83MUcaIJo3BqvKOyFAbOcLayQ5nDG2OXvlLMAykdL5WonaksBw8pRoYQDECuFX-ATReFWy3H7d8cfsMTcWFJc='
"""
