import random

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # Compute d, the modular inverse of e modulo phi(n)
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in plaintext]
    return encrypted_msg

def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted_msg = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(decrypted_msg)
p = 61
q = 53
public_key, private_key = generate_keypair(p, q)
plaintext = "Sabin"
encrypted_msg = encrypt(public_key, plaintext)
decrypted_msg = decrypt(private_key, [2090, 1361, 2778, 2755, 2322])

print("Public Key:", public_key)
print("Private Key:", private_key)
print("Encrypted Message:", encrypted_msg)
print("Decrypted Message:", decrypted_msg)