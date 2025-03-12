import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum_secure_chat import generate_qkd_key, encrypt_message, decrypt_message

def test_generate_qkd_key():
    key = generate_qkd_key()
    assert isinstance(key, bytes) and len(key) == 16  # AES-128 requires 16-byte key

def test_encryption_decryption():
    message = "quantum encryption test"
    key = generate_qkd_key()
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    assert decrypted == message  # decrypted message matches the original
