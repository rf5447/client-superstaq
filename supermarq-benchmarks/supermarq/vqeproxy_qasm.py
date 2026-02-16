# import converters
# import supermarq
# import cirq
# from qiskit import qasm2, qasm3, transpile

# for nq in [3, 4, 5, 7, 9]:
#     for nl in [2, 3, 4, 5, 7, 9]:
#         circ = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()

#         try:
#             circ_qiskit = converters.cirq_to_qiskit(circ)
#             # new line for native gates
#             circ_qiskit = transpile(circ_qiskit, basis_gates=['rx', 'rxx', 'rz'], optimization_level=3)

#             qasm2_string = qasm2.dumps(circ_qiskit)
#             qasm3_string = qasm3.dumps(circ_qiskit)

#             # Use an f-string to make a unique filename
#             filename = f"vqeproxy_{nq}_qubits_{nl}_layers_qasm.txt"
            
#             with open(filename, "w", encoding="utf-8") as f:
#                 f.write(f"###################################################################\n")
#                 f.write(f"# OpenQASM SupermarQ VQEProxy Benchmark ({nq} Qubits, {nl} Layers) #\n")
#                 f.write(f"###################################################################\n")
#                 f.write("--- OpenQASM 2.0 ---\n")
#                 f.write(qasm2_string)
#                 #f.write("\n\n--- OpenQASM 3.0 ---\n")
#                 #f.write(qasm3_string)

#             print(f"Success! File '{filename}' has been created.")

#         except Exception as e:
#             print(f"An error occurred for nq={nq}, nl={nl}: {e}")
import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

for nq in [4, 7, 9]:
    for nl in [1, 2, 3, 4]:
        circuits = supermarq.vqe_proxy.VQEProxy(nq, nl).circuit()

        for idx, circ in enumerate(circuits):

            try:
                circ_qiskit = converters.cirq_to_qiskit(circ)

                circ_qiskit = transpile(
                    circ_qiskit,
                    basis_gates=['rx', 'rxx', 'rz'],
                    optimization_level=3
                )

                qasm2_string = qasm2.dumps(circ_qiskit)
                qasm3_string = qasm3.dumps(circ_qiskit)

                basis_label = "z" if idx == 0 else "x"
                filename = f"vqeproxy_qasm/vqeproxy_{nq}_qubits_{nl}_layers_{basis_label}_basis_qasm.txt"
                
                with open(filename, "w", encoding="utf-8") as f:
                    #f.write("##########################################################################################\n")
                    #f.write(f"# OpenQASM SupermarQ VQEProxy Benchmark ({nq} Qubits, {nl} Layers, {basis_label} Basis) #\n")
                    #f.write("##########################################################################################\n")
                    #f.write("--- OpenQASM 2.0 ---\n")
                    f.write(qasm2_string)

                print(f"Success! File '{filename}' has been created.")

            except Exception as e:
                print(f"An error occurred for nq={nq}, nl={nl}, circ={idx}: {e}")

