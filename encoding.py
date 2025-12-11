from matrixes import G

def encode_vector(vector):
    """
    Encodes a 12-bit vector into a 23-bit Golay codeword using generator matrix G.
    
    Parameters:
        vector: 12-bit information vector (list of int)
    
    Returns:
        23-bit encoded Golay codeword (list of int)
    """
    encoded = [0]*23
    for i in range(12):
        if vector[i] == 1:
            for j in range(23):
                encoded[j] ^= G[i][j]
    return encoded
    
def to_golay_words(byte_array):
    """
    Converts a byte array into a list of 12-bit vectors, preparing for encoding.
    Bytes are converted to a binary string and split into 12-bit groups.
    
    Parameters:
        byte_array: array of bytes (bytearray or bytes)
    
    Returns:
        list of 12-bit vectors (list of lists), 
        last vector is padded with zeros if necessary
    """
    full_binary = ''.join(format(byte, '08b') for byte in byte_array)
    
    binary_vectors = []
    for i in range(0, len(full_binary), 12):
        chunk = full_binary[i:i+12]
        if len(chunk) < 12:
            chunk = chunk.ljust(12, '0')
        binary_vectors.append([int(bit) for bit in chunk])
    
    return binary_vectors
            
    