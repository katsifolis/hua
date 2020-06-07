import random
import json
import sys
import os
from pprint              import pprint
from hashlib             import sha256
from operator            import xor

# Implement BOB #

bool_op = {
    "AND" : lambda x, y: x & y,
    "OR"  : lambda x, y: x | y,
    "XOR" : lambda x, y: x ^ y,
}

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def unary_gate(x, gid):

    # Color bits two for NOT gate because we have only one input
    pbitx = random.randint(0,1)
    pbitz = random.randint(0,1)

    # Constructing the labels
    k0x = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitx).encode('utf-8') 
    k1x = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitx))).encode('utf-8')
    k0z = str(random.getrandbits(128)).encode('utf-8')[:32] + str(pbitz).encode('utf-8')
    k1z = str(random.getrandbits(128)).encode('utf-8')[:32] + str(int(not(pbitz))).encode('utf-8')

    encr    = {}
    encr[0] = sha256(k0x + gid).digest() 
    encr[1] = sha256(k1x + gid).digest()

    assoc = {} # set containing resutls of operation
    counter = 0
    for i in range(0,2):
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

    # Constructing the labels
    k0x  = bytes(os.urandom(32))
    k1x  = bytes(os.urandom(32))
    k0y  = bytes(os.urandom(32))
    k1y  = bytes(os.urandom(32))
    k0z  = bytes(os.urandom(32))
    k1z  = bytes(os.urandom(32))

    encr    = {}
    encr[0] = sha256(k0x + k0y).digest() 
    encr[1] = sha256(k0x + k1y).digest()
    encr[2] = sha256(k1x + k0y).digest()
    encr[3] = sha256(k1x + k1y).digest()


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
        c.append(byte_xor(encr[i], k0z))
#        if assoc[i] == 0:
#            c.append(byte_xor(encr[i], k0z))
#        elif assoc[i] == 1:
#            c.append(byte_xor(encr[i], k1z))

    pprint(c[0].hex())
    pprint(c[1].hex())
    pprint(c[2].hex())
    pprint(c[3].hex())
    random.shuffle(c) # Permute the results

    keys = {}
    keys['x'] = k0x
    keys['y'] = k1y
    keys['z'] = k0z

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


    ko = bob(garbled_tables, keys)

def bob(table, inputs):
    a = []
    for gid, v in table.items():
        for i in range(4):
            x = inputs[gid]['x']
            y = inputs[gid]['y']
            z = inputs[gid]['z']
            a.append(byte_xor(sha256(x + y).digest(), v[i]))
            print(byte_xor(sha256(x + y).digest(), z).hex())

    return a 


with open(sys.argv[1]) as f:
    circ = json.load(f)

aliki(circ)
