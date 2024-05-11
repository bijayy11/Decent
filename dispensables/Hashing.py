import hashlib

def generate_sha_hash(input_string):
    input_bytes = input_string.encode('utf-8')
    
    # Create a new SHA hash object
    sha_hash = hashlib.sha256()
    
    # Update the hash object with the input bytes
    sha_hash.update(input_bytes)
    
    # Get the hexadecimal representation of the hash
    hashed_string = sha_hash.hexdigest()
    
    return hashed_string

if __name__ == "__main__":
    """input_string = "Hello, World!"
    hashed_string = generate_sha_hash(input_string)
    print("SHA hash of '{}' is: {}".format(input_string, hashed_string))"""
