# from credentials_ionq import IONQ_API_KEY
# from qiskit_ionq import IonQProvider

# provider = IonQProvider(IONQ_API_KEY)

# backend_names = [
#     "ionq_simulator",
#     "ionq_qpu",
#     "qpu.forte-1",
#     "qpu.forte-enterprise-1",
#     "qpu.aria-1",
#     "qpu.aria-2",
# ]

# for name in backend_names:
#     try:
#         provider.get_backend(name)
#         print(f"EXISTS: {name}")
#     except Exception as e:
#         print(f"DOES NOT EXIST: {name}: {e}")

# # from credentials_ionq import IONQ_API_KEY
# # from qiskit_ionq import IonQProvider

# # provider = IonQProvider(IONQ_API_KEY)

# # print("Available backends:\n")

# # for backend in provider.backends():
# #     print("Name:", backend.name())
# #     print("Status:", backend.status().status_msg)
# #     print("Operational:", backend.status().operational)
# #     print("Pending jobs:", backend.status().pending_jobs)
# #     print("Options:", backend.options)
# #     print("-" * 50)

import requests

from credentials_ionq import IONQ_API_KEY

BACKENDS = [
    "qpu.forte-1",
    "qpu.forte-enterprise-1",
    "qpu.aria-1",
    "qpu.aria-2",
]

headers = {
    "Authorization": f"apiKey {IONQ_API_KEY}"
}

for backend_name in BACKENDS:
    url = f"https://api.ionq.co/v0.4/backends/{backend_name}"

    response = requests.get(url, headers=headers, timeout=30)

    print("=" * 60)
    print("Requested:", backend_name)

    if response.status_code == 200:
        info = response.json()

        print("Status:", info.get("status"))
        print("Degraded:", info.get("degraded"))
        print("Qubits:", info.get("qubits"))
        print("Average queue time:", info.get("average_queue_time"))
        print("Last updated:", info.get("last_updated"))
        print("Location:", info.get("location"))
        print("Native gates:", info.get("supported_native_gates"))
        print("Characterization ID:", info.get("characterization_id"))
    else:
        print("Could not retrieve backend.")
        print("HTTP status:", response.status_code)
        print("Response:", response.text)