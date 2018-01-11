def encode(I):
	# 1. Apply Predictor for image I
	I_p = apply_predictor(X = A + B - C)

	# 2. Get the diffrence
	I_d = I - I_p

	# 3. Encode I_d by any lossless compression algorithm (Ex. Huffman)
	encoded = run_huffman_encoding(I_d)

	return encoded

def decode(encoded):
	I_d = run_huffman_decoding(encoded)

	I_p = apply_predictor(I_d)

	I = I_d + I_p

	return I
