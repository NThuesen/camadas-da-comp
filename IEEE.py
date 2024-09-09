'''
Retirado de: https://gist.github.com/AlexEshoo/d3edc53129ed010b0a5b693b88c7e0b5
'''
import math

def to_ieee_754_conversion(f, sgn_len=1, exp_len=8, mant_len=23):
    """
    Converts a Floating Point number to its IEEE 754 Floating Point representation as bytes.
    :param f: Floating Point number to be converted
    :param sgn_len: number of sign bits
    :param exp_len: number of exponent bits
    :param mant_len: number of mantissa bits
    :return: IEEE 754 Floating Point representation as bytes
    """
    sign = 0 if f >= 0 else 1
    sign_bits = sign * (2 ** (exp_len + mant_len))

    if abs(f) == float('inf'):
        exponent_bits = 2 ** exp_len - 1
        mantissa_bits = 0
    elif math.isnan(f):
        exponent_bits = 2 ** exp_len - 1
        mantissa_bits = 2 ** (mant_len - 1)  # NaN typically has the leading bit of mantissa set
    else:
        if f == 0.0:
            exponent_bits = 0
            mantissa_bits = 0
        else:
            exponent = int(math.log(abs(f), 2))
            mantissa = abs(f) / (2 ** exponent) - 1
            exponent += (2 ** (exp_len - 1) - 1)
            exponent_bits = exponent
            mantissa_bits = int(mantissa * (2 ** mant_len))

    n = sign_bits | (exponent_bits << mant_len) | mantissa_bits
    return n.to_bytes(4, byteorder='big')



import struct

def from_ieee_754_conversion(ieee_bytes, sgn_len=1, exp_len=8, mant_len=23):
    """
    Converts IEEE 754 Floating Point representation in bytes back to a Floating Point number.
    :param ieee_bytes: IEEE 754 Floating Point representation as bytes
    :param sgn_len: number of sign bits
    :param exp_len: number of exponent bits
    :param mant_len: number of mantissa bits
    :return: Floating Point number
    """
    # Convert the bytes back to an integer
    n = int.from_bytes(ieee_bytes, byteorder='big')
    
    # Extract the sign, exponent, and mantissa
    sign = (n >> (exp_len + mant_len)) & 0x1
    exponent_bits = (n >> mant_len) & ((1 << exp_len) - 1)
    mantissa_bits = n & ((1 << mant_len) - 1)
    
    # Convert back to float
    if exponent_bits == (1 << exp_len) - 1:  # Special case for Inf and NaN
        if mantissa_bits == 0:
            return float('inf') if sign == 0 else -float('inf')
        else:
            return float('nan')
    
    if exponent_bits == 0:  # Subnormal numbers
        exponent = 1 - (1 << (exp_len - 1))
    else:
        exponent = exponent_bits - (1 << (exp_len - 1)) + 1
        mantissa_bits |= 1 << mant_len  # Add the implicit leading 1 for normal numbers
    
    mantissa = mantissa_bits / (1 << mant_len)
    result = (-1) ** sign * mantissa * (2 ** exponent)
    return float("{:.6e}".format(result))

'''
num = 12.213124312431
result = to_ieee_754_conversion(num)
print(result)

volta = from_ieee_754_conversion(int(result, 2))
print(volta)
'''
