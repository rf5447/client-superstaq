import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

for nq in [3, 4, 5, 7, 9]:
    for nr in [2, 3, 4, 5, 7, 9]:
        # bit_state = [0, 1, 0]
        bit_state = [i % 2 for i in range(nq)]
        circ = supermarq.bit_code.BitCode(nq, nr, bit_state).circuit()

        try:
            circ_qiskit = converters.cirq_to_qiskit(circ)
            # new line for native gates
            circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

            qasm2_string = qasm2.dumps(circ_qiskit)
            qasm3_string = qasm3.dumps(circ_qiskit)

            # Use an f-string to make a unique filename
            filename = f"bitcode_qasm/bitcode_{nq}_qubits_{nr}_rounds_qasm.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                #f.write(f"###################################################################\n")
                #f.write(f"# OpenQASM SupermarQ BitCode Benchmark ({nq} Qubits, {nr} Rounds) #\n")
                #f.write(f"###################################################################\n")
                #f.write("--- OpenQASM 2.0 ---\n")
                f.write(qasm2_string)
                #f.write("\n\n--- OpenQASM 3.0 ---\n")
                #f.write(qasm3_string)

            print(f"Success! File '{filename}' has been created.")

        except Exception as e:
            print(f"An error occurred for nq={nq}, nr={nr}: {e}")