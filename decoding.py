from matrixes import H
from matrixes import B

def syndrome(r, H):
    """
    Calculates the syndrome vector for a given received vector.
    
    Parameters:
        r: received vector (list of int)
        H: parity-check matrix (list of lists)
    
    Returns:
        syndrome vector (list of int)
    """
    result = [0] * len(H[0])
    for i, bit in enumerate(r):
        if bit:
            for j in range(len(H[0])):
                result[j] ^= H[i][j]
    return result

def get_weight(vector):
    # Returns the Hamming weight of the vector
    return sum(vector)


def vector_add(v1, v2):
    # Adds two binary vectors (mod 2) XOR
    return [a ^ b for a, b in zip(v1, v2)]

def get_golay_error_vector(received):
    """
    Determines the error vector for Golay code using the decoding algorithm.
    The algorithm can correct up to 3 errors.
    
    Parameters:
        received: received 23-bit vector (list of int)
    
    Returns:
        error vector (list of int) or None if decoding failed
    """
    # Add parity bit to the received vector
    if get_weight(received) % 2 == 0:
        received = received + [1]
    else:
        received = received + [0]
    
    syndromeH = syndrome(received, H)
    
    # Step 1: Check if syndrome weight ≤ 3
    if get_weight(syndromeH) <= 3:
        error_vector = syndromeH + [0] * 12
        return error_vector
    
    # Step 2: check if syndrome + B row has weight ≤ 2
    for i in range(12):
        sbi = vector_add(syndromeH, B[i])
        if get_weight(sbi) <= 2:
            ei = [0] * 12
            ei[i] = 1
            error_vector = sbi + ei
            return error_vector
            
    # Step 3: calculate syndrome with B matrix
    syndromeB = syndrome(syndromeH, B)
    
    # Step 4: if syndromeB weight ≤ 3, errors are in the information part
    if get_weight(syndromeB) <= 3:
        error_vector = [0]*12 + syndromeB
        return error_vector
    
    # Step 5: check if syndromeB + B row has weight ≤ 2
    for i in range(12):
        sbi = vector_add(syndromeB, B[i])
        if get_weight(sbi) <= 2:
            ei = [0] * 12
            ei[i] = 1
            error_vector = ei + sbi
            return error_vector
            
    # If decoding failed (more than 3 errors), return None
    return None
    
def decode_golay_word(received):
    """
    Decodes a single Golay codeword - corrects errors and extracts original information.
    
    Parameters:
        received: received 23-bit Golay codeword (list of int)
    
    Returns:
        decoded 12-bit information vector (list of int) or None if decoding failed
    """
    error_vector = get_golay_error_vector(received)
    if error_vector is None:
        return None
    
    corrected_vector = vector_add(received, error_vector)
    corrected_vector = corrected_vector[:-1]
    return corrected_vector[:12]

def decode_golay_words(vectors):
    """
    Decodes a list of multiple Golay codewords.
    
    Parameters:
        vectors: list of Golay codewords (list of lists)
    
    Returns:
        list of decoded 12-bit vectors (list of lists)
    """
    decoded_vectors = []
    for vector in vectors:
        decoded_vector = decode_golay_word(vector)
        decoded_vectors.append(decoded_vector)
    return decoded_vectors
        
def bits_to_string(binary):
    """
    Converts a binary string to text (UTF-8).
    
    Parameters:
        binary: binary string consisting of '0' and '1' characters (str)
    
    Returns:
        decoded text (str)
    """
    bytes_list = []
    for i in range(0, len(binary), 8):
        byte_chunk = binary[i:i+8]
        if len(byte_chunk) == 8:
            bytes_list.append(int(byte_chunk, 2))

    original_text = bytearray(bytes_list).decode('utf-8')
    return original_text

def reconstruct_text(vectors):
    """
    Reconstructs text from a list of decoded vectors.
    
    Parameters:
        vectors: list of 12-bit vectors (list of lists), 
                 may contain None values for failed decoding
    
    Returns:
        reconstructed text in UTF-8 format (str)
    """
    bytes_list = []
    bit_buffer = 0
    bit_count = 0
    
    for vec in vectors:
        if vec is None:
            vec = [0]*12
        for bit in vec:
            bit_buffer = (bit_buffer << 1) | bit
            bit_count += 1
            
            if bit_count == 8:
                bytes_list.append(bit_buffer)
                bit_buffer = 0
                bit_count = 0
    
    reconstructed_text = bytearray(bytes_list).decode('utf-8', errors='ignore')
    return reconstructed_text

def reconstruct_image(vectors):
    """
    Reconstructs text from a list of decoded vectors.
    
    Parameters:
        vectors: list of 12-bit vectors (list of lists), 
                 may contain None values for failed decoding
    
    Returns:
        reconstructed text in UTF-8 format (str)
    """    
    bytes_list = []
    bit_buffer = 0
    bit_count = 0
    
    for vec in vectors:
        # If vector decoding failed, replace with zeros
        if vec is None:
            vec = [0] * 12
        for bit in vec:
            # Accumulate bits into a byte
            bit_buffer = (bit_buffer << 1) | bit
            bit_count += 1
            
            if bit_count == 8:
                bytes_list.append(bit_buffer)
                bit_buffer = 0
                bit_count = 0
    
    return bytearray(bytes_list)