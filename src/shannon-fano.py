"""Shannon-Fano coding."""

import collections

def decode(encoded_doc, code_list):
    """Shannon-Fano decoding.

    Parameters
    ----------
    encoded_doc: Encoded document.
    code_list: List of <symbol, code>.

    Returns
    -------
    original_doc: Original document.
    """

    original_doc = ''
    curr_code = ''
    for c in encoded_doc:
        curr_code = curr_code + c
        if (has_code(curr_code, code_list)):
            original_doc += symbol_of(curr_code, code_list)
            curr_code = ''
    return original_doc   

def encode(doc):
    """Shannon-Fano encoding.

    Parameters
    ----------
    doc: Document need to encode.

    Returns
    -------
    encoded_doc: Encoded document.
    code_list: List of <Symbol, code>
    """

    # 1. Count symbols in document and we have frequency list
    frequency = count_symbols(doc)

    # 2. Sort the frequency list in descending order
    frequency = sorted(frequency, key=lambda pair: pair[1], reverse=True)

	# 3. Build the encoded table
    code_list = divide_and_assign_code(frequency, 0, len(frequency) - 1, code='')

    # 4. Apply the encoded table to encode the document
    encoded_doc = ''	
    for c in doc:
        encoded_doc = encoded_doc + code_of(c, code_list)
    return encoded_doc, code_list
    
def count_symbols(doc):
    """Count n_times each symbol in symbols appears in the document.

    Parameters
    ----------
    doc: The document.

    Returns
    -------
    frequency: List of <symbol, count>.
    """

    return list(collections.Counter(doc).items())

def divide_and_assign_code(frequency, low, high, code=''):
    """Divide the list and assign code for symbols.

    Parameters
    ----------
    frequency: List of <symbol, count>.
    low: Low index.
    high: High index.
    code: The current code used to assign.

    Returns
    -------
    code_list: List of <symbol, code>.
    """

    # 0. Stop conditions
    if len(frequency) == 1:
        return [(frequency[0][0], '0')]
    if low == high:
        return [(frequency[low][0], code)]
    if low > high:
        return []

	# 1. Divide the frequency list into 2 parts (closest total of count)
    mid = find_mid(frequency, low, high)

	# 2. Assign code and continue to divide until we got one of stop conditions
    code_list_left = divide_and_assign_code(frequency, low, mid, code + '0')
    code_list_right = divide_and_assign_code(frequency, mid + 1, high, code + '1')
    return code_list_left + code_list_right

def find_mid(frequency, low, high):
    """Find the mid index to divide frequency list into 2 parts with closest total count.
    
    Parameters
	----------
	frequency: List of <symbol, count>.
	low: Low index.
	high: High index.

	Returns
	-------
	mid: The index to divide frequency. Two parts are left(low, mid) and right(mid + 1, high).
	"""
    mid = low
    last_delta = abs(sum(frequency, low, low) - sum(frequency, low + 1, high))
    for i in range(low + 1, high):
        sum_left = sum(frequency, low, i)
        sum_right = sum(frequency, i + 1, high)
        curr_delta = abs(sum_left - sum_right)
        if curr_delta >= last_delta:
            mid = i - 1
            break
    return mid

def sum(frequency, low, high):
    """Sum of symbols count.

    Parameters
    ----------
    frequency: List of <symbol, count>
	low: Low index.
	high: High index.
     
    Returns
	-------
	sum: Sum of count from low to high index
    """
    if low > high or low < 0 or high >= len(frequency):
        return 0
    sum = 0
    for i in range(low, high + 1):
        sum = sum + frequency[i][1]
    return sum

def code_of(char, code_list):
    """Get code of a character

    Parameters
    ----------
    char: Character need to decode.
    code_list: List of <symbol, code>.

    Returns
    -------
    code: Code of the character in code_list or empty code if char doesn't exist in code_list
    """
    code = next((code for symbol, code in code_list if symbol == char), '')
    return code

def symbol_of(code_to_find, code_list):
    """Get code of a character

    Parameters
    ----------
    code_to_find: code need to find.
    code_list: List of <symbol, code>.

    Returns
    -------
    code: Code of the character in code_list or empty code if char doesn't exist in code_list
    """
    symbol = next((symbol for symbol, code in code_list if code == code_to_find), '')
    return symbol

def has_code(code_to_find, code_list):
    """Check whether code_list has code_to_find or not

    Parameters
    ----------
    code_to_find: code need to find.
    code_list: List of <symbol, code>.

    Returns
    -------
    True = code_to_find is in code_list
    """
    for symbol, code in code_list:
        if code == code_to_find:
            return True
    return False

def test():
    """Testing with a simple document"""
    doc = 'ABBACAABCECAABADDDE'
    encoded_doc, code_list = encode(doc)
    decoded_doc = decode(encoded_doc, code_list)
    print 'Original doc: {}'.format(doc)
    print 'Encoded doc: {}'.format(encoded_doc)
    print 'Decoded doc: {}'.format(decoded_doc)
    if decoded_doc == doc:
        print 'Decode success.'
    else:
        print 'Decode fail.'

def main():
    """Main."""
    test()
   
if __name__ == '__main__':
    main()
