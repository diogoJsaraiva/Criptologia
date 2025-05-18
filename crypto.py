import random

# Caesar Cipher
def caesar_encrypt(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

# Diffie-Hellman
def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(base, prime, private_key):
    return pow(base, private_key, prime)

def generate_shared_key(received_key, private_key, prime):
    return pow(received_key, private_key, prime)
