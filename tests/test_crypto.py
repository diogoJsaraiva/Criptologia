import builtins
import hashlib
from core import crypto


def test_caesar_cipher_roundtrip():
    original = "Hello, World!"
    shift = 5
    encrypted = crypto.caesar_encrypt(original, shift)
    assert encrypted != original
    decrypted = crypto.caesar_decrypt(encrypted, shift)
    assert decrypted == original


def test_xor_cipher_roundtrip():
    original = "crypto"
    key = 7
    encrypted = crypto.xor_encrypt(original, key)
    assert encrypted != original
    decrypted = crypto.xor_decrypt(encrypted, key)
    assert decrypted == original

def test_hash_function():
    text = "hello"
    assert crypto.calcular_hash(text) == crypto.hashlib.sha256(text.encode()).hexdigest()

def test_simple_hash_function():
    text = "abc"
    expected = str(sum(ord(c) for c in text))
    assert crypto.simple_hash(text) == expected
    
def test_diffie_hellman_shared_key():
    prime = 23
    base = 5
    priv_a = crypto.generate_private_key()
    priv_b = crypto.generate_private_key()
    pub_a = crypto.generate_public_key(base, prime, priv_a)
    pub_b = crypto.generate_public_key(base, prime, priv_b)
    shared_a = crypto.generate_shared_key(pub_b, priv_a, prime)
    shared_b = crypto.generate_shared_key(pub_a, priv_b, prime)
    assert shared_a == shared_b