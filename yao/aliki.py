#!/usr/bin/env python3

# Yao-GC implementation #
from hashlib import sha256
import random
import json
import os
import itertools

assoc = {} # Dictionary of labels and their corresponding value
keys  = [] # Array of Alice's keys

# Helper Function to xor between byte_arrays
def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def unary_gate(x, gid):

    global assoc
    global keys

    # Constructing the labels
    k0x = bytes(os.urandom(32))
    k1x = bytes(os.urandom(32))
    k0z = bytes(os.urandom(32))
    k1z = bytes(os.urandom(32))

    # association so alice can know the output's value
    assoc[k0z] = (0)
    assoc[k1z] = (1)

    # Hashes of the sha digest
    encr    = {}
    encr[0] = sha256(k0x + bytes(gid)).digest() 
    encr[1] = sha256(k1x + bytes(gid)).digest()


    # Appending the values and xor-ing the result
    c       = [] # Garbled table
    c.append(byte_xor(k1z, encr[0]))
    c.append(byte_xor(k0z, encr[1]))
    random.shuffle(c) # Permute the results

    # Alice's input to be sent to bob
    if   x == 1: keys.append(k1x) 
    elif x == 0: keys.append(k0x) 

    # Returns #
    # 1. the garbled table encrypted #
    # 2. the input value encrypted  #
    return c, keys 

def binary_gate(x, y, gid, gtype):

    global assoc
    global keys

    # Constructing the labels
    k0x  = bytes(os.urandom(32)); 
    k1x  = bytes(os.urandom(32)); 
    k0y  = bytes(os.urandom(32)); 
    k1y  = bytes(os.urandom(32)); 
    k0z  = bytes(os.urandom(32)); k1z  = bytes(os.urandom(32))

    # Hash-Digests of inputs
    encr    = {}
    encr[0] = sha256(k0x + k0y + bytes(gid)).digest() 
    encr[1] = sha256(k0x + k1y + bytes(gid)).digest()
    encr[2] = sha256(k1x + k0y + bytes(gid)).digest()
    encr[3] = sha256(k1x + k1y + bytes(gid)).digest()

    c = [] # Garbled table

    # Connect the labels with the actual values
    assoc[k0z] = (0)
    assoc[k1z] = (1)

    # Deciding what type of binary gate this is for each iteration
    if   gtype == 'AND':                 #  AND  #
        c.append(byte_xor(k0z, encr[0])) # 0 0 0 # 
        c.append(byte_xor(k0z, encr[1])) # 0 1 0 #
        c.append(byte_xor(k0z, encr[2])) # 1 0 0 #
        c.append(byte_xor(k1z, encr[3])) # 1 1 1 #

    elif gtype == 'OR':                  #   OR  #
        c.append(byte_xor(k0z, encr[0])) # 0 0 0 # 
        c.append(byte_xor(k1z, encr[1])) # 0 1 1 #
        c.append(byte_xor(k1z, encr[2])) # 1 0 1 #
        c.append(byte_xor(k1z, encr[3])) # 1 1 1 #

    elif gtype == 'XOR':                 #  XOR  #
        c.append(byte_xor(k0z, encr[0])) # 0 0 0 #  
        c.append(byte_xor(k1z, encr[1])) # 0 1 1 #
        c.append(byte_xor(k1z, encr[2])) # 1 0 1 #
        c.append(byte_xor(k0z, encr[3])) # 1 1 0 #

    random.shuffle(c) # Permute the results


    # Alice's input to be sent to bob
    if   x == 1: keys.append(k1x) 
    elif x == 0: keys.append(k0x)
    if   y == 1: keys.append(k1y) 
    elif y == 0: keys.append(k0y)

    # Returns #
    # 1. the garbled table encrypted #
    # 2. the input values encrypted  #
    return c, keys 

def full_adder(x, y, cin = 0):
    """

     Full adder Implementation
     2 XOR Gates
     2 AND Gates
     1 OR  Gate
     Input:  A, B, Cin
     Output: S, Cout

    """
    a = \
        """
        #  TRUTH TABLE  #
        # X Y Ci | Co S #
        # 0 0 0  | 0  0 #
        # 0 1 1  | 1  0 #
        # 1 0 0  | 0  1 #
        # 1 0 1  | 1  0 #
        # 1 1 0  | 1  0 #
        # 1 1 1  | 1  1 #
        # # # # # # # # # 
        """

    # Inputs

    # Hard-coded sequence of gates
    seq = ['XOR', 'XOR', 'AND', 'AND', 'OR']
    # Array of gates' results
    r_values = [-1, -1, -1, -1, -1]

    
    global assoc
    garbled_tables = {}
    key_table      = {}

    # 1st XOR
    garbled_table, key_table[0] = binary_gate(x, y, 0, seq[0])
    garbled_tables[0] = garbled_table
    res = bob(garbled_tables, key_table)
    r_values[4] = ret_val(res)
    del(garbled_tables[0])


    # 2nd XOR
    garbled_table, key_table[1] = binary_gate(r_values[4], cin, 1, seq[1])
    garbled_tables[1] = garbled_table
    res = bob(garbled_tables, key_table)
    r_values[0] = ret_val(res)
    del(garbled_tables[1])

    # 1st AND
    garbled_table, key_table[2] = binary_gate(r_values[4], cin, 2, seq[2])
    garbled_tables[2] = garbled_table
    res = bob(garbled_tables, key_table)
    r_values[1] = ret_val(res)
    del(garbled_tables[2])

    # 2nd AND
    garbled_table, key_table[3] = binary_gate(x, y, 3, seq[3])
    garbled_tables[3] = garbled_table
    res = bob(garbled_tables, key_table)
    r_values[2] = ret_val(res)
    del(garbled_tables[3])

    # OR
    garbled_table, key_table[4] = binary_gate(r_values[1], r_values[2], 4, seq[4])
    garbled_tables[4] = garbled_table
    res = bob(garbled_tables, key_table)
    r_values[3] = ret_val(res)
    del(garbled_tables[4])


    print("Cout: " + str(r_values[3]))
    print("S:    " + str(r_values[0]))
    print()

    return (r_values[3], r_values[0])
    


def ret_val(res):
    for gid, v in res.items():
        for value in v:
            try:
               # pprint("gid: " + str(gid) + " - " + str(assoc[value]))
                return assoc[value]
            except:
               # print('err')
               pass

def aliki():

    # The Input
    a   = "11111"  
    b   = "10110"  
    Cin = 0      # First iteration Cin = 0

    # Array of (len(a) + 1) size 1-bit full adder output
    res      = ['0'] * (len(a) + 1)

    counter = lambda c=itertools.count(): next(c)
    for i in range(len(a)-1, -1, -1): # Addition starts backwards
        x, y = int(a[i], 2), int(b[i], 2)

        print("Iteration {0}".format(counter()))
        Cout, S = full_adder(x, y, Cin)
        Cin = Cout
        res[i+1]  = str(S)
        if i == 0:
            res[i] = str(Cout)
            break

    # Converting the string array to an integer
    sum = 0 
    print("Full Adder outputs : " + str(res))
    res.reverse()
    for i, v in enumerate(res):
        sum += pow(2, i) * int(v)

    print("The sum is " + str(sum))


def bob(table, inputs):
    """

      ciphers     : temporary array for storing the decryption
      cipher_dict : dictionary associating the gate's id with the decryption ciphers

    """
    cipher_dict = {}
    ciphers     = []
    
    for gid, v in table.items():
        x = inputs[gid].pop(0)
        y = inputs[gid].pop(0)
        for i in range(4): # Producing the 4 ciphers and sending back to Alice
            ciphers.append(byte_xor(sha256(x + y + bytes(gid)).digest(), v[i]))

        cipher_dict[gid] = ciphers
        ciphers = [] # 

    return cipher_dict

# Call of the main script
aliki()
