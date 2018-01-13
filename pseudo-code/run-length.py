def encode(doc):
	encoded_doc = empty
	for run in doc:
		count = len(run) # length of run
		symbol = run[0]  # the symbol
		encoded_doc.add(count, symbol)
	return encoded_doc

def decode(encoded_doc):
	decoded_doc = empty
	for count, symbol in encoded_doc:
		decoded_doc = count * symbol
	return decoded_doc
