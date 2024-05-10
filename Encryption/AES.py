from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import RSA
import randomPrimeNumber

"key pair generation for encrypting AES."
public,private=RSA.generate_keypair(randomPrimeNumber.primenumber1,randomPrimeNumber.primenumber2)

def generate_random_key(key_size=32):
  """Generates a random key of specified size (default 32 bytes for AES-256)"""
  backend = default_backend()
  char_array = [chr(byte) for byte in os.urandom(key_size)] # converting bytes in char array
  "2 layer encryption implementation"
  return RSA.encrypt(public,char_array) #returns symmetric key to encrypt and decrypt the message 

def encrypt(key, plaintext):
  """Encrypts plaintext using AES in CBC mode with PKCS#7 padding"""
  key = key[:32]  # Enforce 32-byte key for AES-256
  iv = os.urandom(16)  # Generate random initialization vector (IV)

  cipher = ciphers.Cipher(
      algorithms.AES(key),
      modes.CBC(iv),
      backend=default_backend()
  )
  encryptor = cipher.encryptor()
  padder = padding.PKCS7(cipher.algorithm.block_size).padder()  # Dynamic padding
  padded_data = padder.update(plaintext) + padder.finalize()
  ciphertext = iv + encryptor.update(padded_data) + encryptor.finalize()

  return ciphertext


def decrypt(key, ciphertext):
    """Decrypts ciphertext using AES in CBC mode with PKCS#7 unpadding"""
    key = key[:32]  # Enforce 32-byte key for AES-256
    iv = ciphertext[:16]  # Extract IV from the beginning of ciphertext
    ciphertext = ciphertext[16:]  # Remove IV from the payload

    cipher = ciphers.Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    return plaintext



keyinArray=RSA.decrypt(private,generate_random_key()) # decrypting AES key
key = bytes(ord(char) for char in keyinArray) # converting to byte-like datatype
plaintext = "This is a Secret Message".encode()
ciphertext = encrypt(key, plaintext) # encrypting actual message
decrypted_text = decrypt(key, ciphertext) # decrypting message

print(f"Plaintext: {plaintext.decode()}")
print(f"Ciphertext (hex): {ciphertext.hex()}")
print(f"Decrypted text: {decrypted_text.decode()}")
print(f"Key: {key}")