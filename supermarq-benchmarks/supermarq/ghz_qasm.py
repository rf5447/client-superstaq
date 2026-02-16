# # convert GHZ circuit with 5 qubits to QASM 2.0 and QASM 3.0

# import converters
# # import GHZ
# import supermarq
# from benchmarks import ghz
# from qiskit import qasm2, qasm3
# import cirq

# # 1. Generate the circuit
# circ = supermarq.ghz.GHZ(5).circuit()
# circ_qiskit = converters.cirq_to_qiskit(circ)

# # # 2a. Use the QASM output module
# # qasm_output = cirq.qasm(circ)

# # print("--- Cirq Generated OpenQASM 2.0 ---")
# # print(qasm_output)

# # 2. Export to OpenQASM 2.0 (The new way)
# qasm2_string = qasm2.dumps(circ_qiskit)
# print("--- OpenQASM 2.0 ---")
# print(qasm2_string)

# # 3. Export to OpenQASM 3.0
# qasm3_string = qasm3.dumps(circ_qiskit)
# print("\n--- OpenQASM 3.0 ---")
# print(qasm3_string)

import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

for n in [3, 4, 5, 7, 9]:
    circ = supermarq.ghz.GHZ(n).circuit()

    try:
        circ_qiskit = converters.cirq_to_qiskit(circ)
         # new line for native gates
        circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

        qasm2_string = qasm2.dumps(circ_qiskit)
        qasm3_string = qasm3.dumps(circ_qiskit)

        # Use an f-string to make a unique filename
        filename = f"ghz_qasm/ghz_{n}_qubits_qasm.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            #f.write(f"###############################################\n")
            #.write(f"# OpenQASM SupermarQ GHZ Benchmark ({n} Qubits) #\n")
            #f.write(f"###############################################\n")
            #f.write("--- OpenQASM 2.0 ---\n")
            f.write(qasm2_string)
            #f.write("\n\n--- OpenQASM 3.0 ---\n")
            #f.write(qasm3_string)

        print(f"Success! File '{filename}' has been created.")

    except Exception as e:
        print(f"An error occurred for n={n}: {e}")