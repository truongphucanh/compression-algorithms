"""
Runlength encoding module
"""

from re import sub

def encode(text):
    """
    Encode a document (text).

    Parameters
    ----------
    text : string
        Original document.

    Returns
    -------
    encoded: string
        Encoded document.

    """
    encoded = sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1), text)
    return encoded

def decode(text):
    """
    Encode a document (text).

    Parameters
    ----------
    text : string
        Encoded document.

    Returns
    -------
    origin: string
        Original document.

    """
    origin = sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)), text)
    return origin

def encode_file(in_file, out_file, ratio_file = None):
    """
    Encode a document file.

    Parameters
    ----------
    in_file : string
        Input file (need to encode).
    out_file : string 
        Output file (encoded file).
    ratio_file : string
        Compression ratio
    """
    origin = ''
    f = open(in_file, 'r')
    if f.mode == 'r':
        origin = f.read()
    f.close()

    encoded = encode(origin)

    f = open(out_file, 'w')
    f.write(encoded)
    f.close()

    if ratio_file != None:
        ratio = len(origin) * 1.0 / len(encoded)
        f = open(ratio_file, 'a')
        f.write('Runlength, {}, {}\n'.format(in_file, str(ratio)))
        f.close()

def test():
    """
    Just for testing.
    """
    origin = str('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')
    print 'Origin doc:\t {}'.format(origin)
    encoded = encode(origin)
    print 'Encoded doc:\t {}'.format(encoded)
    decoded = decode(encoded)
    print 'Decoded doc:\t {}'.format(decoded)
    assert decoded == origin

if __name__ == "__main__":
    N_FILES = 16
    ratio = '../bin/ratio.csv'
    for i in range(0, 16):
        origin_file = '../data/text/{}.txt'.format(str(i))
        encoded_file = '../bin/runlength/text/{}.txt'.format(str(i))
        encode_file(origin_file, encoded_file, ratio)
    print 'Encode done.'
