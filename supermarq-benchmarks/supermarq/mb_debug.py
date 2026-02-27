import numpy as np
import cirq
import supermarq
from supermarq.simulation import get_ideal_counts

# Loop through the requested qubit counts
for n in [3, 4, 5]:
    print(f"--- Ideal Counts for Mermin-Bell (n={n}) ---")
    
    # 1. Initialize the Mermin-Bell benchmark
    # The benchmark defines the circuit logic.
    mb = supermarq.mermin_bell.MerminBell(n)
    
    # 2. Retrieve the circuit
    # This circuit is used for both simulation and hardware execution.
    circuit = mb.circuit()
    
    # 3. Calculate ideal probabilities using the simulation function
    # get_ideal_counts performs a noiseless statevector simulation.
    # It returns bitstrings in big-endian order.
    ideal_probs = get_ideal_counts(circuit)
    
    # 4. Display results
    # Only non-zero probabilities are printed for clarity.
    for bitstr, prob in sorted(ideal_probs.items()):
        if prob > 0:
            print(f"State: |{bitstr}> | Probability: {prob:.4f}")
    print("-" * 40)