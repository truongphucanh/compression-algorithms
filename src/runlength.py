""" Runlength encoding module. """

from itertools import groupby
import pickle

def encode(document):
    """ Encode a document (document).

    Parameters
    ----------
    document : string.
        Original document.

    Returns
    -------
    encoded: list<int, char>.
        Encoded document as a list of pair <length of run, symbol>.

    """
    encoded = [(len(list(run)), symbol) for symbol, run in groupby(document)]
    return encoded

def decode(lst):
    """ Encode a document (document).

    Parameters
    ----------
    lst : list<int, char>
        Encoded document as a list of pair <length of run, symbol>.

    Returns
    -------
    origin: string
        Original document.

    """
    origin = ''.join(symbol * n_times for n_times, symbol in lst)
    return origin

def test():
    """ Just for testing. """
    origin = str('WWWWWW3333WWBWWWW55555W62WWBBBWWWWW0-1W-1WWWW-1-1-1-1WWWWWWWWWWBWWWWWWWWWWWWWW')
    print 'Origin doc:\t {}'.format(origin)
    encoded = encode(origin)
    print 'Encoded doc:\t {}'.format(encoded)
    decoded = decode(encoded)
    print 'Decoded doc:\t {}'.format(decoded)
    assert decoded == origin

def encode_file(in_file, out_file, ratio_file=None):
    """ Encode a document file.

    Parameters
    ----------
    in_file : Input file (need to encode).
    out_file : Output file (encoded file).
    ratio_file : Compression ratio file.
    """
    with open(in_file, 'r') as file_reader:
        document = file_reader.read()

    encoded_list = [(len(list(run)), symbol) for symbol, run in groupby(document)]
    with open(out_file, 'wb') as file_writer:
        pickle.dump(encoded_list, file_writer)

    if ratio_file != None:
        encoded_str = ''.join(str(run_length) + str(symbol) for run_length, symbol in encoded_list)
        ratio = len(document) * 1.0 / len(encoded_str)
        with open(ratio_file, 'a') as file_writer:
            file_writer.write('{},{},{},{}\n'.format(in_file, len(document) * 8, len(encoded_str) * 8, ratio))

def decode_file(in_file, out_file):
    """ Encode a document file.

    Parameters
    ----------
    in_file : string
        pkl file, stored an encoded_list.
    out_file : string 
        Output file (decoded file).
    ratio_file : string
        Compression ratio
    """
    with open(in_file, 'rb') as file_reader:
        encoded = pickle.load(file_reader)
    decoded = decode(encoded)    
    file_writer = open(out_file, 'w')
    file_writer.write(decoded)
    file_writer.close()

def validate(origin_file, decoded_file):
    """Validate a decoded file.

    Returns
    -------
    Whether decoded file has the same content with the original file or not.
    """

    with open(origin_file, 'r') as file_reader:
        origin_doc = file_reader.read()

    with open(origin_file, 'r') as file_reader:
        decoded_doc = file_reader.read()

    return origin_doc == decoded_doc


if __name__ == "__main__":
    #test()
    N_FILES = 16
    for i in range(0, N_FILES):
        print 
        origin_file = '../data/text/{}.txt'.format(str(i))
        encoded_file = '../bin/runlength/encode/text/{}.pkl'.format(str(i))
        decoded_file = '../bin/runlength/decode/text/{}.txt'.format(str(i))
        encode_file(origin_file, encoded_file, ratio_file='../bin/runlength/ratio.csv')
        decode_file(encoded_file, decoded_file)
        print 'i = {}: {}'.format(i, validate(origin_file=origin_file, decoded_file=decoded_file))
    print 'Done.'
