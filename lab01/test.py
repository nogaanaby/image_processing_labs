#!/usr/bin/python3

from itertools import cycle
from hashlib import md5

# the real flag is on the server
FLAG = b'MagTF{????????????????????}'
# f=b'MagTF{'
# c=b'}'
#
# d='0'*8*6 + '1'*20*8 + '0'*8

def xor(a, b):
    return bytes(aa ^ bb for aa, bb in zip(a, b))


def main():
    inp = bytes.fromhex(input('Enter some data to sign:\n'))

    signature = md5(xor(inp, cycle(FLAG))).digest()

    print(signature.hex())
main()