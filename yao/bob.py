import socket
import base64
import pickle
import random
import string
from hashlib import sha256
from cryptography.fernet import Fernet
from pprint import pprint

HOST = 'localhost'
PORT = 6969

def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)


def bob(garbled_table, x, y):

    val = 0
    for k, v in garbled_table.items():
        for value in v:
            try:
                val = decrypt(y, decrypt(x, value))
            except:
                pass

    return val



    








