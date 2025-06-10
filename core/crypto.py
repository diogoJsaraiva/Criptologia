import random
import hashlib

# Caesar Cipher
def caesar_encrypt(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

# XOR Cipher
def xor_encrypt(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def xor_decrypt(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def cifrar_mensagem(mensagem, metodo, extra):
    if metodo == "caesar":
        shift = int(extra) if extra and extra.isdigit() else 3
        return caesar_encrypt(mensagem, shift)
    elif metodo == "xor":
        key = int(extra) if extra and extra.isdigit() else 42
        return xor_encrypt(mensagem, key)
    else:
        return mensagem

def decifrar_mensagem(mensagem, metodo, extra):
    if metodo == "caesar":
        shift = int(extra) if extra and extra.isdigit() else 3
        return caesar_decrypt(mensagem, shift)
    elif metodo == "xor":
        key = int(extra) if extra and extra.isdigit() else 42
        return xor_decrypt(mensagem, key)
    else:
        return mensagem

# Diffie-Hellman (mantém para tua lógica de chave partilhada)
def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(base, prime, private_key):
    return pow(base, private_key, prime)

def generate_shared_key(received_key, private_key, prime):
    return pow(received_key, private_key, prime)
    
def calcular_hash(mensagem):
    return hashlib.sha256(mensagem.encode()).hexdigest()