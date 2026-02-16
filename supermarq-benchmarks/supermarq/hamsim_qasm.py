import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

for nq in [4, 7, 11, 12, 13, 16, 20]:
    for steps in [1, 3, 4, 5, 7]:
        ts = 1
        tt = steps * ts

        circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()

        try:
            circ_qiskit = converters.cirq_to_qiskit(circ)
            # new line for native gates
            circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

            qasm2_string = qasm2.dumps(circ_qiskit)
            qasm3_string = qasm3.dumps(circ_qiskit)

            # Use an f-string to make a unique filename
            filename = f"hamsim_qasm/hamsim_{nq}_qubits_{ts}_ts_{tt}_tt_qasm.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                #f.write(f"#####################################################################################################\n")
                #f.write(f"# OpenQASM SupermarQ HamiltonianSimulation Benchmark ({nq} Qubits, {ts} Timesteps, {tt} Total Time) #\n")
                #f.write(f"#####################################################################################################\n")
                #f.write("--- OpenQASM 2.0 ---\n")
                f.write(qasm2_string)
                #f.write("\n\n--- OpenQASM 3.0 ---\n")
                #f.write(qasm3_string)

            print(f"Success! File '{filename}' has been created.")

        except Exception as e:
            print(f"An error occurred for nq={nq}, ts={ts}, tt={tt}: {e}")