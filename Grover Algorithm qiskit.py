
try:
   
    from qiskit_aer import Aer
    print(" استفاده از qiskit_aer (جدیدترین نسخه)")
except ImportError:
    try:
       
        from qiskit.providers.aer import Aer
        print("استفاده از qiskit.providers.aer (نسخه قدیمی)")
    except ImportError:
       
        from qiskit.providers.basic_provider import BasicAer
        Aer = BasicAer
        print(" استفاده از BasicAer (شبیه‌ساز پایه)")

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import MCXGate
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt


DATA_SIZE = 16 
TARGET_INDEX = 5 
SHOTS = 1000  


n_qubits = int(np.ceil(np.log2(DATA_SIZE)))
iterations = int(np.pi * np.sqrt(DATA_SIZE) / 4)

print(f" اندازه دیتابیس: {DATA_SIZE} (نیاز به {n_qubits} کیوبیت)")
print(f" اندیس هدف: {TARGET_INDEX} (معادل باینری: {format(TARGET_INDEX, f'0{n_qubits}b')})")
print(f" تعداد تکرارهای گروور: {iterations}")


qc = QuantumCircuit(n_qubits, n_qubits)


qc.h(range(n_qubits))
qc.barrier()


def apply_oracle():
    binary_target = format(TARGET_INDEX, f'0{n_qubits}b')
    
 
    for qubit, bit in enumerate(reversed(binary_target)):
        if bit == '0':
            qc.x(qubit)
   
    mcx = MCXGate(n_qubits-1)
    qc.h(n_qubits-1)
    qc.append(mcx, list(range(n_qubits)))
    qc.h(n_qubits-1)
    
 
    for qubit, bit in enumerate(reversed(binary_target)):
        if bit == '0':
            qc.x(qubit)


def apply_diffuser():
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    
    mcx = MCXGate(n_qubits-1)
    qc.h(n_qubits-1)
    qc.append(mcx, list(range(n_qubits)))
    qc.h(n_qubits-1)
    
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))


for _ in range(iterations):
    apply_oracle()
    qc.barrier()
    apply_diffuser()
    qc.barrier()


qc.measure(range(n_qubits), range(n_qubits))


print("\nمدار کوانتومی کامل:")
print(qc.draw(output='text', fold=-1))


try:
    backend = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, backend)
    job = backend.run(compiled_circuit, shots=SHOTS)
    result = job.result()
    counts = result.get_counts(qc)


    most_probable = max(counts, key=counts.get)
    found_index = int(most_probable, 2)

    print("\nنتایج اجرا:")
    print(f" تعداد اجراها: {SHOTS}")
    print(f" اندیس پیدا شده: {found_index} (هدف: {TARGET_INDEX})")
    print(f" دقت الگوریتم: {counts[most_probable]/SHOTS*100:.1f}%")
    print("\nتوزیع کامل نتایج:")
    print(counts)

    
    plot_histogram(counts, title="توزیع نتایج جستجوی گروور")
    plt.show()

except Exception as e:
    print(f"\n خطا در اجرای مدار: {str(e)}")
    print("لطفاً مطمئن شوید qiskit-aer نصب شده است:")
    print("pip install qiskit-aer")