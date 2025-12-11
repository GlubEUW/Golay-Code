# B matrix (12x12)
# Used to construct the generator H matrix
B = [
    [1,1,0,1,1,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,0,0,1,0,1,1],
    [0,1,1,1,0,0,0,1,0,1,1,1],
    [1,1,1,0,0,0,1,0,1,1,0,1],
    [1,1,0,0,0,1,0,1,1,0,1,1],
    [1,0,0,0,1,0,1,1,0,1,1,1],
    [0,0,0,1,0,1,1,0,1,1,1,1],
    [0,0,1,0,1,1,0,1,1,1,0,1],
    [0,1,0,1,1,0,1,1,1,0,0,1],
    [1,0,1,1,0,1,1,1,0,0,0,1],
    [0,1,1,0,1,1,1,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,0]
]

# I12 - 12x12 identity matrix
I12 = [[1 if i == j else 0 for j in range(12)] for i in range(12)]

# B_no_last - B matrix without the last column (12x11)
# Used to construct the generator matrix G
B_no_last = [row[:-1] for row in B]

# G - Generator matrix for Golay (23,12,7) code (12x23)
# Structure: G = [I12 | B_no_last]
# Used to encode 12-bit information vectors into 23-bit codewords
G = [I12[i] + B_no_last[i] for i in range(12)]

# Structure: H = I12 + B
# Used to calculate syndromes and detect/correct errors
H = I12 + B
