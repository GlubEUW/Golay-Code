
def channel_transfer(data, error_prob):
    """
    Simulates data transmission through a noisy channel with a specified error probability.
    Each bit can be flipped with probability error_prob.
    
    Parameters:
        data: vector of bits to transmit (list of int)
        error_prob: error probability for each bit (float, 0-1)
    
    Returns:
        transmitted vector with random errors (list of int)
    """
    import random
    transferred_data = []
    # Iterate through each bit
    for bit in data:
        # With probability error_prob, flip the bit (0->1 or 1->0)
        if random.random() < error_prob:
            transferred_data.append(1 - bit)
        else:
            transferred_data.append(bit)
    return transferred_data

def error_positions(original, received):
    """
    Determines positions where the original and received vectors differ (error locations).
    
    Parameters:
        original: original vector (list of int)
        received: received vector (list of int)
    
    Returns:
        list of indices where errors occurred (list of int)
    """
    positions = []
    for i in range(len(original)):
        if original[i] != received[i]:
            positions.append(i)
    return positions

def transfer_vectors(vectors, p):
    """
    Transmits a list of multiple vectors through a noisy channel.
    Each vector is transmitted separately with the same error probability.
    
    Parameters:
        vectors: list of vectors to transmit (list of lists)
        p: error probability for each bit (float, 0-1)
    
    Returns:
        list of transmitted vectors with errors (list of lists)
    """
    transferred_vectors = []
    for vector in vectors:
        transferred_vector = channel_transfer(vector, p)
        transferred_vectors.append(transferred_vector)
    return transferred_vectors
