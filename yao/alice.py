import json
import bob
import struct
import sys
import socket
import base64
import pickle
import random
import string
import os
from hashlib import sha256
from cryptography.fernet import Fernet
from pprint import pprint


# Globals
HOST = 'localhost' # Local connection through sockets
PORT = 6969 # The port to connect to

bool_gate = {
    "AND" : lambda x, y: x & y,
    "OR"  : lambda x, y: x | y,
    "XOR" : lambda x, y: x ^ y,
    "NOT" : lambda x, : not(x),
}


# Generating random labels
l = {}

def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt(key, data):
    f = Fernet(key)
    return f.decrypt(data)


def gen_garbled_table(circ):

    g_tables = {}
    gates = circ['gates']

    for n, g in enumerate(gates):

        op = g['type']
        print(op)
        ciphers = []
        if op == 'AND':
            ciphers.append(encrypt(l['k0x'], encrypt(l['k0y'], l['k0z'])))  
            ciphers.append(encrypt(l['k0x'], encrypt(l['k1y'], l['k0z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k0y'], l['k0z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k1y'], l['k1z'])))
        if op == 'OR':
            ciphers.append(encrypt(l['k0x'], encrypt(l['k0y'], l['k0z'])))  
            ciphers.append(encrypt(l['k0x'], encrypt(l['k1y'], l['k1z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k0y'], l['k1z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k1y'], l['k1z'])))
        if op == 'XOR':
            ciphers.append(encrypt(l['k0x'], encrypt(l['k0y'], l['k0z'])))  
            ciphers.append(encrypt(l['k0x'], encrypt(l['k1y'], l['k1z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k0y'], l['k1z'])))
            ciphers.append(encrypt(l['k1x'], encrypt(l['k1y'], l['k0z'])))
        if op == 'NOT':
            ciphers.append(encrypt(l['k0x'], ['k1z']))  
            ciphers.append(encrypt(l['k1x'], ['k0z']))

        random.shuffle(ciphers) # permute the contents of garbled gate

        g_tables[n] = ciphers

    return g_tables


def alice(circ):

    # --------------------------------------------------- #
    # Encrypting the truth table                          #
    # --------------------------------------------------- #

    # Alice's input
    a_inputs = circ['alice']

    for w in range(65,len(a_inputs)+65):
        for label in range(0, 2):
            l["k{0}{1}".format(chr(w), label)] = keypair()

    pprint(l)
    a_out, b_out = 0, 0

    
    if   a == 0: a_out = l['A0']
    elif a != 0: a_out = l['A1']

    if   b == 0: b_out = l['B0']
    elif b != 0: b_out = l['B1']

    garble_tables = gen_garbled_table(circ)

    # -------------------------- 3 - 4 -------------------#
    # Sending the Garbled gate serialized through sockets #
    # And also the keys of the input.                     #
    # --------------------------------------------------- #

    # object to send
    z = bob.bob(garble_tables, a_out, b_out)
    if z == l['k0z']: print(0)
    elif z == l['k1z']: print(1)
    
# Loading the circuit from a JSON file
with open(sys.argv[1]) as f:
    circ = json.load(f)

alice(circ)

