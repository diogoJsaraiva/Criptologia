import builtins
from core import crypto


def test_caesar_cipher_roundtrip():
    original = "Hello, World!"
    shift = 5
    encrypted = crypto.caesar_encrypt(original, shift)
    assert encrypted != original
    decrypted = crypto.caesar_decrypt(encrypted, shift)
    assert decrypted == original


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