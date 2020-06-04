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
            encr = encrypt(w[chr(c)][i], int(not(i)).to_bytes(1, byteorder='big'))
            ciphers.append(encr)

    random.shuffle(ciphers) # permute the contents of garbled gate

    return ciphers

def gen_garbled_table(w, inputs, op, c):

    a, b = inputs[0], inputs[1]

    ciphers = []

    for i in range(0,2):
        for j in range(0, 2):
            
            #encr = encrypt(w[chr(c)][a], encrypt(w[chr(c+1)][b], int(bool_gate[op](a, b)).to_bytes(1, byteorder='big')))
            encr = encrypt(w[chr(c)][i], encrypt(w[chr(c+1)][j], bytes(w[chr(c+2)][bool_gate[op](i, j)])))
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
    c        = 65 # start labeling from a 
    

    # Constructing the labels
    for w in range(N):
        for b in range(0, 2):
            wires['{0}'.format(chr(65+w))] = {0: Fernet.generate_key(), 1: Fernet.generate_key()}


    for g in gates:

        if g['type'] == 'NOT':
            ciphers = gen_garbled_table_not(wires,  g['in'], c)
            g_tables[g['id']] = ciphers
            keys[g['id']] = [wires[chr(c)][a_inputs[0]]]
        else:
            ciphers = gen_garbled_table(wires, g['in'], g['type'], c)
            g_tables[g['id']] = ciphers
            keys[g['id']] = [wires[chr(c)][a_inputs[0]], wires[chr(c+1)][a_inputs[1]]]

        c = c + 2
        a_inputs = a_inputs[2:]
        



    # -------------------------- 3 - 4 -------------------#
    # Sending the Garbled gate over to bob(Evaluator)     #
    # And also the keys of the input.                     #
    # --------------------------------------------------- #

    # object to send
    z = bob.bob(g_tables, keys) # Sending the garbled circuit
    c = 0
    for k, v in wires.items():
        for val in v.items():
            if z[c] == val[1]:
                print(val[0])

            c = not(c)

    pprint(wires)


    
# Loading the circuit from a JSON file
with open(sys.argv[1]) as f:
    circ = json.load(f)

alice(circ)

