import random
import hashlib

# Caesar Cipher
def caesar_encrypt(text, shift):
    if not 1 <= shift <= 25:
        raise ValueError("Shift must be between 1 and 25")
    return ''.join(chr((ord(c) + shift) % 256) for c in text)

def caesar_decrypt(text, shift):
    if not 1 <= shift <= 25:
        raise ValueError("Shift must be between 1 and 25")
    return ''.join(chr((ord(c) - shift) % 256) for c in text)

# XOR Cipher
def xor_encrypt(text, key):
    if not 0 <= key <= 255:
        raise ValueError("XOR key must be between 0 and 255")
    return ''.join(chr(ord(c) ^ key) for c in text)

def xor_decrypt(text, key):
    if not 0 <= key <= 255:
        raise ValueError("XOR key must be between 0 and 255")
    return ''.join(chr(ord(c) ^ key) for c in text)

#vigenere  Cipher
def vigenere_encrypt(texto, chave):
    resultado = []
    chave = chave.upper()
    chave_len = len(chave)
    for i, char in enumerate(texto):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(chave[i % chave_len]) - 65
            c = (ord(char) - offset + k) % 26 + offset
            resultado.append(chr(c))
        else:
            resultado.append(char)
    return ''.join(resultado)
    
def shared_key_to_vigenere_key(shared_key):
    """Converte um número inteiro (ex: shared_key) numa string alfabética para Vigenère."""
    key_str = ""
    while shared_key > 0:
        key_str += chr(97 + (shared_key % 26))  # gera letras de 'a' a 'z'
        shared_key //= 26
    return key_str or "a"  # fallback no caso de shared_key = 0

def vigenere_decrypt(texto, chave):
    resultado = []
    chave = chave.upper()
    chave_len = len(chave)
    for i, char in enumerate(texto):
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            k = ord(chave[i % chave_len]) - 65
            c = (ord(char) - offset - k) % 26 + offset
            resultado.append(chr(c))
        else:
            resultado.append(char)
    return ''.join(resultado)

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
    
# Simple hash: sum of ASCII values
def simple_hash(mensagem):
    return str(sum(ord(c) for c in mensagem))

def calcular_hash_sha256(mensagem: str) -> str:
    return hashlib.sha256(mensagem.encode()).hexdigest()

def verificar_hash(mensagem: str, hash_recebido: str) -> bool:
    hash_calculado = calcular_hash_sha256(mensagem)
    return hash_calculado == hash_recebido