import socket
import base64
import pickle
import random
import string
from hashlib import sha256
from cryptography.fernet import Fernet
from pprint import pprint

def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)


def bob(garbled_table, inputs):

    val = 0
    out = []

    for k, v in garbled_table.items():
        x = inputs[k]
        print(x)

        if len(inputs.items()) < 2:
            y = None

        for value in v:
            try:
                if y == None:
                    val = decrypt(x, value)
                    out.append(val)
                else:
                    val = decrypt(y, decrypt(x, value))
                    out.append(val)

            except:
                print('r')
                pass

    return out
