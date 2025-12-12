import sys
import time

import encoding
import decoding
import transfer

import os

def input_vector():
    """
    Prompts the user to input a 12-bit vector from the console.
    Validates that the input contains exactly 12 bits (0s and 1s).
    
    Parameters:
        None
    
    Returns:
        12-bit vector entered by the user (list of int)
    """
    vector_length = 12
    
    print("Enter the vector of size 12, consisting of 0s and 1s, separated by spaces")
    while True:
        vector_input = input()
        vector = [int(x) for x in vector_input.split()]
        if len(vector) != vector_length:
            print(f"Vector must be of length {vector_length}, try again")
        else:
            break
    return vector

def input_text():
    """
    Prompts the user to input multi-line text from the console.
    Input continues until EOF (Ctrl+Z on Windows, Ctrl+D on Unix).
    
    Parameters:
        None
    
    Returns:
        text entered by the user (str)
    """
    print("Enter the text to encode (ctrl + Z then Enter to save):")  
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    
    contents_str = '\n'.join(contents)
    return contents_str
    
def input_image():
    """
    Prompts the user to input a path to a BMP image file.
    Validates that the file exists and is a BMP format.
    
    Parameters:
        None
    
    Returns:
        raw bytes of the BMP image file (bytes)
    """
    while True:
        print("Enter the path to the BMP image file:")
        file_path = input().strip()

        # check if file exists
        if not os.path.isfile(file_path):
            print("File does not exist, please try again")
            continue
        # check if file is BMP
        if not file_path.lower().endswith('.bmp'):
            print("File is not a BMP image, please try again")
            continue

        # try to read the file
        try:
            with open(file_path, "rb") as f:
                raw_bytes = f.read()
            return raw_bytes
        except OSError:
            print("Could not read the file, please try again")
            continue

def error_probability():
    """
    Prompts the user to input the channel error probability.
    Validates that the value is between 0 and 1.
    
    Parameters:
        None
    
    Returns:
        error probability (float)
    """
    while True:
        try:

            print("Enter channel error probability p (0-1)")
            p = float(input())

            if p < 0 or p > 1:
                print("Probability must be between 0 and 1, try again")
            else:
                break
        except ValueError:
            print("Invalid input, please enter a number between 0 and 1, try again")
            
    return p

def change_vector(vector):
    """
    Allows the user to manually flip bits in a vector at specified positions.
    
    Parameters:
        vector: vector to modify (list of int), modified in place
    
    Returns:
        None (modifies vector in place)
    """
    print("Enter the positions to change (0-22), separated by spaces (or press Enter to skip)")
    while True:
        try:
            positions_input = input()
            # If user presses Enter without input, skip modification
            if positions_input.strip() == "":
                return
            
            positions = [int(x) for x in positions_input.split()]
            # Validate that all positions are within valid range
            if any(pos < 0 or pos > 22 for pos in positions):
                print("Positions must be between 0 and 22, try again")
                continue
            
            # Flip bits at specified positions
            for pos in positions:
                vector[pos] ^= 1
            
            break
            
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces, try again")
        except Exception as e:
            print(f"An error occurred: {e}. Please try again")


def count_corrupted_vectors(original_vectors, result_vectors):
    """
    Counts the number of corrupted vectors and total bit errors.
    Compares original vectors with result vectors after transmission/decoding.
    
    Parameters:
        original_vectors: list of original 12-bit vectors (list of lists)
        result_vectors: list of received/decoded vectors (list of lists), may contain None
    
    Returns:
        tuple: (number of corrupted vectors, total bit errors)
    """
    corrupted = 0
    total_bit_errors = 0
    
    for orig, result in zip(original_vectors, result_vectors):
        # If decoding failed completely, count all 12 bits as errors
        if result is None:
            corrupted += 1
            total_bit_errors += 12
        # If vectors differ, count the specific bit errors
        elif orig != result:
            corrupted += 1
            bit_errors = sum(1 for i in range(len(orig)) if orig[i] != result[i])
            total_bit_errors += bit_errors
    
    return corrupted, total_bit_errors


def main():
    """
    Main program loop. Presents a menu with three scenarios:
    1. Encode and decode a single 12-bit vector with optional manual errors
    2. Encode text with Golay code and compare results with/without encoding
    3. Encode a BMP image with Golay code and compare results with/without encoding
    
    Parameters:
        None
    
    Returns:
        0 on successful exit
    """
    
    while True:
        print("Enter which scenario to run (1-3) or q to quit:")
        print("1: Encode and decode a 12-bit vector with optional manual errors.")
        print("2: Encode text with Golay code.")
        print("3: Encode a BMP image with Golay code.")

        input_scenario = input()
        
        if input_scenario == '1':
            print("You have chosen scenario 1")
            # Get user inputs
            vector = input_vector()            
            p = error_probability()
            
            # Encode the vector using Golay code
            encoded_vector = encoding.encode_vector(vector)
            print(f"Encoded vector: {encoded_vector}")
            
            # Simulate transmission over a channel with error probability p
            transferred_vector = transfer.channel_transfer(encoded_vector, p)
            print(f"Transferred vector: {transferred_vector}")
            
            
            print(f"Error positions: {transfer.error_positions(encoded_vector, transferred_vector)}")
            
            
            print("You can now manually change bits in the transferred vector.")
            change_vector(transferred_vector)
            print(f"Modified transferred vector: {transferred_vector}")
            # Decode the received vector
            decoded_vector = decoding.decode_golay_word(transferred_vector)
            print(f"Decoded vector: {decoded_vector}")
            
            
            
            
        elif input_scenario == '2':
            print("You have chosen scenario 2")
            # Get user inputs
            text = input_text()
            p = error_probability()
            
            # Convert text to byte array and then to 12-bit vectors
            byte_array = bytearray(text, 'utf-8')
            text_vectors = encoding.to_golay_words(byte_array)
            
            print(f"\nText converted to {len(text_vectors)} vectors")
            
            print("\n--- WITHOUT ENCODING ---")
            # Simulate transmission without encoding
            transferred_vectors_no_enc = transfer.transfer_vectors(text_vectors, p)
            
            corrupted_no_enc, bit_errors_no_enc = count_corrupted_vectors(text_vectors, transferred_vectors_no_enc)
            
            reconstructed_text = decoding.reconstruct_text(transferred_vectors_no_enc)
            
            # Print statistics
            print(f"Corrupted vectors: {corrupted_no_enc}/{len(text_vectors)} ({corrupted_no_enc/len(text_vectors)*100:.2f}%)")
            print(f"Total bit errors: {bit_errors_no_enc}")
            print(f"Average bit errors per vector: {bit_errors_no_enc/len(text_vectors):.3f}")
            print("Reconstructed text:")
            print(reconstructed_text)
            
            print("\n--- WITH GOLAY ENCODING ---")
            # Encode the vectors using Golay code
            encoded_vectors = []
            for vector in text_vectors:
                encoded_vectors.append(encoding.encode_vector(vector))
            
            # Simulate transmission with encoding
            transferred_vectors_enc = transfer.transfer_vectors(encoded_vectors, p)
            decoded_vectors = decoding.decode_golay_words(transferred_vectors_enc)
            
            # Count corrupted vectors and bit errors
            corrupted_with_enc, bit_errors_with_enc = count_corrupted_vectors(text_vectors, decoded_vectors)
            
            reconstructed_text = decoding.reconstruct_text(decoded_vectors)
            
            # Print statistics
            print(f"Corrupted vectors: {corrupted_with_enc}/{len(text_vectors)} ({corrupted_with_enc/len(text_vectors)*100:.2f}%)")
            print(f"Total bit errors: {bit_errors_with_enc}")
            print(f"Average bit errors per vector: {bit_errors_with_enc/len(text_vectors):.3f}")
            print("Reconstructed text:")
            print(reconstructed_text)

            
                
                
            
        elif input_scenario == '3':
            print("You have chosen scenario 3")
            # Get user inputs
            image_bytes = input_image()
            p = error_probability()
            
            # Separate BMP header (first 54 bytes) from pixel data
            metadata = image_bytes[:54]
            image_bytes = image_bytes[54:]
            
            # Convert image byte data to 12-bit vectors
            image_vectors = encoding.to_golay_words(image_bytes)
            print(f"\nImage converted to {len(image_vectors)} vectors")
            
            print("\n--- WITHOUT ENCODING ---")
            start_time = time.time()
            
            # Simulate transmission without encoding
            transferred_vectors_no_enc = transfer.transfer_vectors(image_vectors, p)
            
            corrupted_no_enc, bit_errors_no_enc = count_corrupted_vectors(image_vectors, transferred_vectors_no_enc)
            
            reconstructed_bytes = metadata + decoding.reconstruct_image(transferred_vectors_no_enc)
            
            with open("reconstructed_image.bmp", "wb") as f:
                f.write(reconstructed_bytes)
                
            time_no_enc = time.time() - start_time
            
            # Print statistics
            print(f"Corrupted vectors: {corrupted_no_enc}/{len(image_vectors)} ({corrupted_no_enc/len(image_vectors)*100:.2f}%)")
            print(f"Total bit errors: {bit_errors_no_enc}")
            print(f"Average bit errors per vector: {bit_errors_no_enc/len(image_vectors):.3f}")
            print(f"Processing time: {time_no_enc:.2f} seconds")
            print("Saved as 'reconstructed_image.bmp'")

            print("\n--- WITH GOLAY ENCODING ---")
            start_time = time.time()
            
            # Encode the vectors using Golay code
            encoded_vectors = []
            for vector in image_vectors:
                encoded_vectors.append(encoding.encode_vector(vector))
            
            # Simulate transmission with encoding
            transferred_vectors_enc = transfer.transfer_vectors(encoded_vectors, p)
            decoded_vectors = decoding.decode_golay_words(transferred_vectors_enc)
            
            # Count corrupted vectors and bit errors
            corrupted_with_enc, bit_errors_with_enc = count_corrupted_vectors(image_vectors, decoded_vectors)
            
            
            # Reconstruct the image bytes
            reconstructed_bytes = metadata + decoding.reconstruct_image(decoded_vectors)
            with open("reconstructed_encoded_image.bmp", "wb") as f:
                f.write(reconstructed_bytes)
            
            time_with_enc = time.time() - start_time
            
            #Print statistics
            print(f"Corrupted vectors: {corrupted_with_enc}/{len(image_vectors)} ({corrupted_with_enc/len(image_vectors)*100:.2f}%)")
            print(f"Total bit errors: {bit_errors_with_enc}")
            print(f"Average bit errors per vector: {bit_errors_with_enc/len(image_vectors):.3f}")
            print(f"Processing time: {time_with_enc:.2f} seconds")
            print("Saved as 'reconstructed_encoded_image.bmp'")
                         
        
        # Exit
        elif(input_scenario == 'q'):
            print("Exiting program")
            quit()
        else:
            print("Please enter a number between 1 and 3 or q to quit")    
        
 
    return 0

if __name__ == "__main__":
    main()