import sys
import os

# add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from quantum_secure_chat import generate_qkd_key, encrypt_message, decrypt_message

def test_generate_qkd_key():
    key = generate_qkd_key()
    assert isinstance(key, bytes) and len(key) == 16  # AES-128 key is 16 bytes

def test_encryption_decryption():
    message = "Quantum Encryption Test"
    key = generate_qkd_key()
    encrypted = encrypt_message(message, key)
    decrypted = decrypt_message(encrypted, key)
    assert decrypted == message  # encryption & decryption work correctly
