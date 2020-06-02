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

    for k, v in garbled_table.items():
        x = inputs[k][0]
        y = inputs[k][1]
        print(x)
        print(y)
        #pprint(garbled_table[k])
        for value in v:
            try:
                if y == -1:
                    val = decrypt(x, value)
                    break
                else:
                    val = decrypt(y, decrypt(x, value))
                    print("AAAAAAAAAAAA")
                    print(val)

            except:
                print('r')
                pass

    return val
