import random
import json
import sys
from pprint              import pprint
from cryptography.fernet import Fernet
from os                  import urandom
from hashlib             import sha256
from operator            import xor


# Implement BOB #

bool_op = {
    "AND" : lambda x, y: x & y,
    "OR"  : lambda x, y: x | y,
    "XOR" : lambda x, y: x ^ y,
}

def encrypt(key, data):
    f = Fernet(key)
    return f.encrypt(data)

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def unary_gate(x, gid):

    # Color bits two for NOT gate because we have only one input
    pbitx = random.randint(0,1)
    pbitz = random.randint(0,1)

    # Constructing the labels
    k0x  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitx).encode('utf-8') 
    k1x  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitx))).encode('utf-8')
    k0z  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitz).encode('utf-8')
    k1z  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitz))).encode('utf-8')

    encr    = {}
    encr[0] = sha256(k0x + gid).digest() 
    encr[1] = sha256(k1x + gid).digest()

    assoc = {} # set containing resutls of operation
    counter = 0
    for i in range(0,2):
            op = int(not(i))
            assoc[counter] = op
            counter += 1

    # Constructing the encryption
    c = [] # Garbled table
    for i in range(2):
        if assoc[i] == 0:
            c.append(byte_xor(encr[i], k0z).hex())
        elif assoc[i] == 1:
            c.append(byte_xor(encr[i], k1z).hex())

    random.shuffle(c) # Permute the results

    keys = {}
    if   x == 1: keys['x'] = k1x
    elif x == 0: keys['x'] = k0x

    # Returns #
    # 1. the garbled table encrypted #
    # 2. the input value encrypted  #
    return c, keys 

def binary_gate(x, y, gid, gtype):

    # Color bits
    pbity = random.randint(0,1)
    pbitx = random.randint(0,1)
    pbitz = random.randint(0,1)

    # Constructing the labels
    k0x  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitx).encode('utf-8') 
    k1x  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitx))).encode('utf-8')
    k0y  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbity).encode('utf-8')
    k1y  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbity))).encode('utf-8')
    k0z  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitz).encode('utf-8')
    k1z  = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitz))).encode('utf-8')

    encr    = {}
    encr[0] = sha256(k0x + k0y + gid).digest() 
    encr[1] = sha256(k0x + k1y + gid).digest()
    encr[2] = sha256(k1x + k0y + gid).digest()
    encr[3] = sha256(k1x + k1y + gid).digest()

    assoc = {} # set containing resutls of operation
    counter = 0
    for i in range(0,2):
        for j in range(0,2):
            op = bool_op[gtype](i, j)
            assoc[counter] = op
            counter += 1
    
    # Constructing the encryption
    c = [] # Garbled table
    for i in range(4):
        if assoc[i] == 0:
            c.append(byte_xor(encr[i], k0z).hex())
        elif assoc[i] == 1:
            c.append(byte_xor(encr[i], k1z).hex())

    random.shuffle(c) # Permute the results
    print(c)

    keys = {}
    if   x == 1: keys['x'] = k1x
    elif x == 0: keys['x'] = k0x
    if   y == 1: keys['y'] = k1y
    if   y == 0: keys['y'] = k0y

    # Returns #
    # 1. the garbled table encrypted #
    # 2. the input values encrypted  #
    return c, keys 


def aliki(circ):
    circuit        = {}
    gates          = circ['gates']
    a_input        = circ['alice']
    garbled_tables = {}
    keys           = {}

    for g in gates:
        circuit = []
        g_input = g['in']
        g_id    = g['id'].to_bytes(1, byteorder='big')
        g_type  = g['type']
        if len(g_input) < 2:
            x                               = g_input[0]
            garbled_table, keys[g_id.hex()] = unary_gate(x, g_id)
        else:
            x             = g_input[0]
            y             = g_input[1]
            garbled_table, keys[g_id.hex()] = binary_gate(x, y, g_id, g_type)

        garbled_tables[g_id.hex()] = garbled_table


    bob(garbled_tables, keys)

def bob(table, inputs):

    for t, v in table.items():
        for val in v:
    



with open(sys.argv[1]) as f:
    circ = json.load(f)

aliki(circ)

