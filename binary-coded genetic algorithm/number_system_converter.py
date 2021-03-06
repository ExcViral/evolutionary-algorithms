# Functions to take care of binary to float and back to binary conversions

# The following functions are not my implementations, they have been taken from:
#   https://stackoverflow.com/questions/8751653/how-to-convert-a-binary-string-into-a-float-value

# import necessary libraries

import struct
from bitarray import bitarray
import numpy as np

# ======================================================================================================================
# ===== Helper functions ===============================================================================================
# ======================================================================================================================


def int_to_bytes(n, minlen=0):  # Helper function
    """ Int/long to byte string.
        Python 3.2+ has a built-in int.to_bytes() method that could be
        used instead, but the following is portable.
    """
    nbits = n.bit_length() + (1 if n < 0 else 0)  # +1 for any sign bit.
    nbytes = (nbits+7) // 8  # Number of whole bytes.
    b = bytearray()
    for _ in range(nbytes):
        b.append(n & 0xff)
        n >>= 8
    if minlen and len(b) < minlen:  # Zero padding needed?
        b.extend([0] * (minlen-len(b)))
    return bytearray(reversed(b))  # High bytes first.

# ======================================================================================================================
# ===== Main functions =================================================================================================
# ======================================================================================================================


def bin_to_float(b):
    """ Convert bitarray (binary string) to a float. """
    b = b.to01()
    bf = int_to_bytes(int(b, 2), 8)  # 8 bytes needed for IEEE 754 binary64.
    return struct.unpack('>d', bf)[0]


def float_to_bin(value):  # For testing.
    """ Convert float to 64-bit bitarray (binary string). """
    [d] = struct.unpack(">Q", struct.pack(">d", value))
    # return '{:064b}'.format(d)
    return bitarray('{:064b}'.format(d))
