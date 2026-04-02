# from supermarq import converters
# import supermarq
# import cirq
# from qiskit import qasm2, qasm3, transpile

# for nq in [4, 7, 11, 12, 13, 16, 20]:
#     for steps in [1, 3, 4, 5, 7]:
#         ts = 1
#         tt = steps * ts

#         circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()

#         try:
#             circ_qiskit = converters.cirq_to_qiskit(circ)
#             # new line for native gates
#             circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

#             qasm2_string = qasm2.dumps(circ_qiskit)
#             qasm3_string = qasm3.dumps(circ_qiskit)

#             # Use an f-string to make a unique filename
#             filename = f"hamsim_qasm/hamsim_{nq}_qubits_{ts}_ts_{tt}_tt_qasm.txt"
            
#             with open(filename, "w", encoding="utf-8") as f:
#                 #f.write(f"#####################################################################################################\n")
#                 #f.write(f"# OpenQASM SupermarQ HamiltonianSimulation Benchmark ({nq} Qubits, {ts} Timesteps, {tt} Total Time) #\n")
#                 #f.write(f"#####################################################################################################\n")
#                 #f.write("--- OpenQASM 2.0 ---\n")
#                 f.write(qasm2_string)
#                 #f.write("\n\n--- OpenQASM 3.0 ---\n")
#                 #f.write(qasm3_string)

#             print(f"Success! File '{filename}' has been created.")

#         except Exception as e:
#             print(f"An error occurred for nq={nq}, ts={ts}, tt={tt}: {e}")

from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, transpile, QuantumCircuit
from qiskit.circuit.library import RXXGate, RXGate, RZGate # Added specific gate imports
import numpy as np

for nq in [4, 7, 11, 12, 13, 16, 20]:
    for steps in [1, 3, 4, 5, 7]:
        ts = 1
        tt = steps * ts

        circ = supermarq.hamiltonian_simulation.HamiltonianSimulation(nq, ts, tt).circuit()

        try:
            circ_qiskit = converters.cirq_to_qiskit(circ)
            
            # 1. Transpile to basis gates (Optimization level 3)
            # This handles the initial mapping and heavy optimization
            circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

            # 2. Slice RXX gates to fit the [-pi/4, pi/4] constraint
            # We recreate the circuit to ensure the data structure is clean
            new_circ = QuantumCircuit(*circ_qiskit.qregs, *circ_qiskit.cregs)
            limit = np.pi / 4

            for circuit_instruction in circ_qiskit.data:
                inst = circuit_instruction.operation
                qargs = circuit_instruction.qubits
                cargs = circuit_instruction.clbits
                
                if isinstance(inst, RXXGate):
                    theta = float(inst.params[0])
                    # Decomposition logic
                    num_chunks = int(abs(theta) // limit)
                    remainder = abs(theta) % limit
                    sign = np.sign(theta)

                    for _ in range(num_chunks):
                        new_circ.append(RXXGate(sign * limit), qargs)
                    
                    if remainder > 1e-10:
                        new_circ.append(RXXGate(sign * remainder), qargs)
                else:
                    # Keep RX, RZ, and any other gates as they are
                    new_circ.append(inst, qargs, cargs)
            
            circ_qiskit = new_circ

            # 3. Export to QASM
            qasm2_string = qasm2.dumps(circ_qiskit)
            filename = f"hamsim_qasm/hamsim_{nq}_qubits_{ts}_ts_{tt}_tt_qasm.txt"
            
            # Note: Ensure the 'hamsim_qasm' directory exists!
            with open(filename, "w", encoding="utf-8") as f:
                f.write(qasm2_string)

            print(f"Success! File '{filename}' has been created.")

        except Exception as e:
            print(f"An error occurred for nq={nq}, ts={ts}, tt={tt}: {e}")