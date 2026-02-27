from qiskit_ibm_runtime import QiskitRuntimeService
 
QiskitRuntimeService.save_account(
token="uEwpfCne9rG2zWo_e-afRPi_dBrZdJQIszdFRf7xANH8", # Use the 44-character API_KEY you created and saved from the IBM Quantum Platform Home dashboard
overwrite="True",
channel="ibm_cloud",

#instance="<CRN>", # Optional
)

