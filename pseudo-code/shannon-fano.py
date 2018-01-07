def decode(encoded_doc, code_list):
	"""Shannon-Fanon decoding.

	Parameters
	----------
	encoded_doc: Encoded document.
	code_list: List of <symbol, code>.

	Returns
	-------
	original_doc: The original document.
	"""
	original_doc = ''	
	curr_code = ''
	for c in encoded_doc:
		curr_code = curr_code + c
		if (code_list.has(currcode)):
			original_doc = code_list.code_of(curr_code)
			curr_code = ''
	return original_doc

def encode(doc, symbols):
	"""Shannon-Fanon encoding.

	Parameters
	----------
	doc: The document.
	symbols: Set of symbols.

	Returns
	-------
	encoded_doc: The encoded document.
	code_list: List of <symbol, code>
	"""
	# 1. Count symbols in document and we have frequency list
	frequency<symbol, count> = count_symbol_in(doc)

	# 2. Sort the frequency list in descending order
	frequency = sort(frequency)

	# 3. Build the encoded table
	code_list<symbol, code> = divide_and_assign_code(frequency, 0, len(frequency) - 1, code='') 

	# 4. Apply the encoded table to encode the document
	encoded_doc = ''	
	for c in doc:
		encoded_doc = encoded_doc + code_of(c, encoded_table)
	return encoded_doc, code_list

def divide_and_assign_code(frequency, low, high, code=''):
	"""Divide the list and assign code for symbols.
	
	Parameters
	----------
	frequency: List of <symbol, count>.
	low: Low index.
	high: High index.
	code: The current code assign (default is '' means code of root is empty)

	Returns
	-------
	code_list: List of <symbol, code>	
	"""
	
	# 0. Stop conditions
	if (len(frequency) == 1) return [(frequency[0].symbol), code]
	if (low == high) return [(frequency[low].symbol, code)]
	if (low > high) return empty_list

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
		if (curr_delta >= last_delta):
			mid = i - 1
			break
	return mid
	
