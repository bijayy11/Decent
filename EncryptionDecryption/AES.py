from cryptography.hazmat.primitives import ciphers
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


def generate_random_key(key_size=32):
  """Generates a random key of specified size (default 32 bytes for AES-256)"""
  backend = default_backend()
  return os.urandom(key_size)


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
  unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()  # Dynamic unpadding
  plaintext = unpadder.update(ciphertext) + unpadder.finalize()

  return plaintext


# Example usage
key = generate_random_key()
plaintext = "This is a secret message".encode()
ciphertext = encrypt(key, plaintext)
decrypted_text = decrypt(key, ciphertext)

print(f"Plaintext: {plaintext.decode()}")
print(f"Ciphertext (hex): {ciphertext.hex()}")
print(f"Decrypted text: {decrypted_text.decode()}")
