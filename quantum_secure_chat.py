import numpy as np
import os
from qiskit import QuantumCircuit, Aer, execute
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

# generate random bits (alice's raw key)
def generate_random_bits(length):
    return np.random.randint(2, size=length)

# generate random measurement bases
def generate_random_bases(length):
    return np.random.randint(2, size=length)

# prepare quantum states based on bits and bases
def prepare_qubits(bits, bases):
    qubits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)  
        if basis == 1:
            qc.h(0)  
        qubits.append(qc)
    return qubits

# simulate bob's measurement of qubits
def measure_qubits(qubits, bases):
    results = []
    simulator = Aer.get_backend('aer_simulator')
    for qc, basis in zip(qubits, bases):
        if basis == 1:
            qc.h(0)  
        qc.measure(0, 0)
        job = execute(qc, simulator, shots=1, memory=True)
        result = job.result().get_memory()[0]
        results.append(int(result))
    return np.array(results)

# alice and bob sift the key by comparing bases
def sift_key(alice_bits, alice_bases, bob_results, bob_bases):
    matching_indices = np.where(alice_bases == bob_bases)[0]
    key = alice_bits[matching_indices]  
    return key

# generate 128-bit key from quantum key distribution
def generate_qkd_key(num_bits=128):
    alice_bits = generate_random_bits(num_bits)
    alice_bases = generate_random_bases(num_bits)
    qubits = prepare_qubits(alice_bits, alice_bases)

    bob_bases = generate_random_bases(num_bits)
    bob_results = measure_qubits(qubits, bob_bases)

    final_key_bits = sift_key(alice_bits, alice_bases, bob_results, bob_bases)
    
    key_bytes = bytes(np.packbits(final_key_bits)[:16])  

    print(f"\n🔑 Shared Quantum Key (AES-128 Compatible): {key_bytes.hex()}")
    return key_bytes

# encrypt messages using AES-GCM
def encrypt_message(message, key):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    tag = encryptor.tag  
    
    encrypted_data = base64.b64encode(iv + tag + ciphertext).decode()
    return encrypted_data

# decrypt messages using AES-GCM
def decrypt_message(encrypted_data, key):
    decoded_data = base64.b64decode(encrypted_data)
    
    iv = decoded_data[:12]
    tag = decoded_data[12:28]
    ciphertext = decoded_data[28:]

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    
    return decrypted_message.decode()

# generate quantum-secure AES key
quantum_key = generate_qkd_key()

# secure quantum messaging test
alice_message = "Hello Lakshman! This is a quantum-secure message."
encrypted_msg = encrypt_message(alice_message, quantum_key)
decrypted_msg = decrypt_message(encrypted_msg, quantum_key)

print(f"\n📩 Original Message: {alice_message}")
print(f"🔐 Encrypted Message: {encrypted_msg}")
print(f"🔓 Decrypted Message: {decrypted_msg}")
