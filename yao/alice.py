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
from uuid import uuid1
from hashlib import sha256
from cryptography.fernet import Fernet
from pprint import pprint


## TODO

# Encrypt the output so bob doesn't know the value

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

def gen_garbled_FA():
    pass

    
def gen_garbled_table_not(w, inputs, c):

    a  = inputs[0]
    ciphers = []

    for i in range(0,2):
            encr = encrypt(w['a'][i], int(not(i)).to_bytes(8, byteorder='big'))
            ciphers.append(encr)


    random.shuffle(ciphers) # permute the contents of garbled gate

    return ciphers

def gen_garbled_table(w, inputs, op, c):

    a, b = inputs[0], inputs[1]

    ciphers = []

    for i in range(0,2):
        for j in range(0, 2):
            print(bool_gate[op](i, j))
            encr = encrypt(w[chr(c).lower()][i], encrypt(w[chr(c).lower()][j], int(bool_gate[op](inputs[i], inputs[j])).to_bytes(1, byteorder='big')))
            ciphers.append(encr)


    random.shuffle(ciphers) # permute the contents of garbled gate

    return ciphers


def alice(circ):

    # --------------------------------------------------- #
    # Encrypting the truth table                          #
    # --------------------------------------------------- #

    # Alice's input
    a_inputs = circ['alice']
    print(a_inputs)
    gates    = circ['gates']
    N        = len(a_inputs) + len(circ['out']) # number of wires
    wires    = {}
    keys     = {}
    g_tables = {}
    a, b, c  = 0, 0, 0
    rnd_bit  = lambda: random.randint(0,1)
    c        = 65 # start labeling from a 
    

    # Constructing the labels
    for w in range(N):
        for b in range(0, 2):
            wires['{0}'.format(chr(65+w)).lower()] = {0: Fernet.generate_key(), 1: Fernet.generate_key()}


    for g in gates:
        if g['type'] == 'NOT':
            ciphers = gen_garbled_table_not(wires,  g['in'], c)
            g_tables[g['id']] = ciphers
            keys[g['id']] = [wires[chr(c).lower()][rnd_bit()]]
        else:
            ciphers = gen_garbled_table(wires, g['in'], g['type'], c)
            g_tables[g['id']] = ciphers
            keys[g['id']] = [wires[chr(c).lower()][rnd_bit()], wires[chr(c+1).lower()][rnd_bit()]]

        c = c + 2
        
    pprint(wires)
    pprint(keys)
    pprint(g_tables)



    # -------------------------- 3 - 4 -------------------#
    # Sending the Garbled gate over to bob(Evaluator)     #
    # And also the keys of the input.                     #
    # --------------------------------------------------- #

    # object to send
    z = bob.bob(g_tables, keys) # Sending the garbled circuit


    
# Loading the circuit from a JSON file
with open(sys.argv[1]) as f:
    circ = json.load(f)

alice(circ)

