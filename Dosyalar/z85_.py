import sys
import struct

PY3 = sys.version_info[0] >= 3
# Z85CHARS 85 sembol icin taban tablo
Z85CHARS = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
# Z85MAP [0,84]  Z85CHARS in saysisal karsiligi
Z85MAP = dict([(c, idx) for idx, c in enumerate(Z85CHARS)])

_85s = [ 85**i for i in range(5) ][::-1]

def encode(rawbytes):
   
    if len(rawbytes) % 4:
        raise ValueError("uzunluk 4'un katı olmalı, %i" % len(rawbytes))
    
    nvalues = len(rawbytes) / 4
    
    values = struct.unpack('>%dI' % nvalues, rawbytes)
    encoded = []
    for v in values:
        for offset in _85s:
            encoded.append(Z85CHARS[(v // offset) % 85])
    
    if PY3:
        return bytes(encoded)
    else:
        return b''.join(encoded)

def decode(z85bytes):
    if PY3 and isinstance(z85bytes, str):
        try:
            z85bytes = z85bytes.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('Dizi bagimsiz degiskeni yalnizca ASCII karakterleri icermelidir')

    if len(z85bytes) % 5:
        raise ValueError("Z85 uzunluğu 5'in katı olmalıdır, %i" % len(z85bytes))
    
    nvalues = len(z85bytes) / 5
    values = []
    for i in range(0, len(z85bytes), 5):
        value = 0
        for j, offset in enumerate(_85s):
            value += Z85MAP[z85bytes[i+j]] * offset
        values.append(value)
    return struct.pack('>%dI' % nvalues, *values)