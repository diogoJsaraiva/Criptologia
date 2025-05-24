import random

# Caesar Cipher
def caesar_encrypt(text, shift):
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

def cifrar_mensagem(mensagem, metodo, extra):
    if metodo == "caesar":
        shift = int(extra) if extra and extra.isdigit() else 3
        return caesar_encrypt(mensagem, shift)
    else:
        return mensagem

def decifrar_mensagem(mensagem, metodo, extra):
    if metodo == "caesar":
        shift = int(extra) if extra and extra.isdigit() else 3
        return caesar_decrypt(mensagem, shift)
    else:
        return mensagem

# Diffie-Hellman (mantém para tua lógica de chave partilhada)
def generate_private_key():
    return random.randint(2, 100)

def generate_public_key(base, prime, private_key):
    return pow(base, private_key, prime)

def generate_shared_key(received_key, private_key, prime):
    return pow(received_key, private_key, prime)