from supermarq import converters
import supermarq
import cirq
from qiskit import qasm2, qasm3, transpile

for nq in [4, 5, 7, 11, 12, 13, 16, 20]:

    circ = supermarq.qaoa_fermionic_swap_proxy.QAOAFermionicSwapProxy(nq).circuit()

    try:
        circ_qiskit = converters.cirq_to_qiskit(circ)

        # new line for native gates
        circ_qiskit = transpile(
            circ_qiskit,
            basis_gates=['rx', 'rxx', 'rz'],
            optimization_level=3
        )

        qasm2_string = qasm2.dumps(circ_qiskit)
        qasm3_string = qasm3.dumps(circ_qiskit)

        # Use an f-string to make a unique filename
        filename = f"fswap_qasm/fswap_{nq}_qubits_qasm.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(qasm2_string)

        print(f"Success! File '{filename}' has been created.")

    except Exception as e:
        print(f"An error occurred for nq={nq}: {e}")
