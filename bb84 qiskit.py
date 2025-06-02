from qiskit import QuantumCircuit
import random
import numpy as np


try:
    
    from qiskit_aer import Aer
    from qiskit import transpile
    backend = Aer.get_backend('qasm_simulator')
    def run_circuit(qc):
        return transpile(qc, backend), backend.run(transpile(qc, backend), shots=1).result()
    USE_AER = True
except ImportError:
    try:
      
        from qiskit.providers.aer import Aer
        from qiskit import execute
        backend = Aer.get_backend('qasm_simulator')
        def run_circuit(qc):
            return qc, execute(qc, backend, shots=1).result()
        USE_AER = True
    except ImportError:
        
        from qiskit.providers.basic_provider import BasicAer
        from qiskit import execute
        backend = BasicAer.get_backend('qasm_simulator')
        def run_circuit(qc):
            return qc, execute(qc, backend, shots=1).result()
        USE_AER = True

def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.randint(0, 1) for _ in range(length)]

def prepare_qubits(qc, bits, bases, qubit_indices):
    for i in range(len(bits)):
        if bits[i] == 1:
            qc.x(qubit_indices[i])
        if bases[i] == 1:
            qc.h(qubit_indices[i])

def measure_qubits(qc, bases, qubit_indices, classical_indices):
    for i in range(len(bases)):
        if bases[i] == 1:
            qc.h(qubit_indices[i])
        qc.measure(qubit_indices[i], classical_indices[i])

def sift_keys(alice_bits, bob_bits, alice_bases, bob_bases):
    return [alice_bits[i] for i in range(len(alice_bases)) 
            if alice_bases[i] == bob_bases[i]]


length = 20
alice_bits = generate_random_bits(length)
alice_bases = generate_random_bases(length)
bob_bases = generate_random_bases(length)


qc = QuantumCircuit(length, length)
prepare_qubits(qc, alice_bits, alice_bases, range(length))
measure_qubits(qc, bob_bases, range(length), range(length))


transpiled_qc, result = run_circuit(qc)
counts = result.get_counts()
bob_bits = [int(bit) for bit in list(counts.keys())[0]][::-1]


sifted_key = sift_keys(alice_bits, bob_bits, alice_bases, bob_bases)


print("نتایج پروتکل BB84:")
print(f"کلید نهایی: {sifted_key}")
print(f"طول کلید: {len(sifted_key)}")


print("\nمدار کوانتومی:")
print(qc.draw(output='text'))