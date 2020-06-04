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

    # Encryptiong without optimization techniques e.g Point-and-Permute
    for i in range(0,2):
            encr = encrypt(w[chr(c)][i], bytes(w[chr(c+1)][int(not(i))]))
            ciphers.append(encr)

    random.shuffle(ciphers) # permute the contents of garbled gate

    return ciphers

def gen_garbled_table(w, inputs, op, c):

    a, b = inputs[0], inputs[1]

    ciphers = []

    # Encryptiong without optimization techniques e.g Point-and-Permute
    for i in range(0,2):
        for j in range(0, 2):
            encr = encrypt(w[chr(c)][i], encrypt(w[chr(c+1)][j], bytes(w[chr(c+2)][bool_gate[op](a, b)])))
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
    tmp = 0
    for g in gates:
        if g['type'] == "NOT":
            tmp += 1
        else:
            tmp += 2


    N        = tmp + len(circ['out']) # number of wires
    assoc    = {}
    wires    = {}
    keys     = {}
    ins      = {}
    g_tables = {}
    c        = 65 # start labeling from a 
    r        = lambda : random.randint(0,1)
    

    # Constructing the labels.
    for w in range(N):
        wires['{0}'.format(chr(65+w))] = (Fernet.generate_key(), Fernet.generate_key())


    # Constructing the Garbled tables.
    for g in gates:
        if g['type'] == 'NOT':
            a = g['in'][0]
            bit_out = int(not(a))
            lab_a = chr(c) + str(a)
            lab_b = chr(c+1) + str(bit_out)

            assoc[lab_a] = wires[chr(c)][r()]
            assoc[lab_b] = wires[chr(c+1)][r()]

            keys[g['id']] = assoc[lab_a]
            ciphers = gen_garbled_table_not(wires,  g['in'], c)
            g_tables[g['id']] = ciphers
            c += 1
        else:
            keys[g['id']] = (wires[chr(c)][r()], wires[chr(c+1)][r()])
            ciphers = gen_garbled_table(wires, g['in'], g['type'], c)
            g_tables[g['id']] = ciphers
            c += 2

        a_inputs = a_inputs[2:]
        



    # -------------------------- 3 - 4 -------------------#
    # Sending the Garbled gate over to bob(Evaluator)     #
    # And also the keys of the input.                     #
    # --------------------------------------------------- #
    # object to send

    z = bob.bob(g_tables, keys) # Sending the garbled circuit
    print()
    print(z)

    
# Loading the circuit from a JSON file
with open(sys.argv[1]) as f:
    circ = json.load(f)

alice(circ)

