
# circuits/random.py
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit_aer import AerSimulator

def build_random_circuit(num_bits: int) -> QuantumCircuit:
    """
    Build a circuit that prepares a uniform superposition across `num_bits` qubits
    and measures them. Each shot produces a random `num_bits`-bit string.
    """
    qc = QuantumCircuit(num_bits, num_bits)
    # Put every qubit into superposition
    for q in range(num_bits):
        qc.h(q)
    # Measure each qubit to its corresponding classical bit
    qc.measure(range(num_bits), range(num_bits))
    return qc

def run_qrng(num_bits: int, shots: int, backend=None):
    """
    Run the QRNG circuit and return a list of integer values (0 .. 2^num_bits - 1)
    sampled `shots` times.

    Returns:
      counts_dict: raw counts mapping bitstring -> frequency
      samples: list of integers (len = shots)
    """
    if backend is None:
        backend = AerSimulator()

    qc = build_random_circuit(num_bits)
    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=shots)
    result = job.result()
    counts = result.get_counts()  # mapping bitstring -> frequency

    # Convert counts into a list of integer samples (expand counts)
    samples = []
    for bitstr, freq in counts.items():
        # Qiskit returns bitstrings with qubit 0 as the rightmost char in many setups,
        # but typical Aer returns bitstrings with most-significant-left (msb=left).
        # We want to treat the bitstring as binary with leftmost being MSB:
        # e.g. '101' -> 5
        int_val = int(bitstr, 2)
        samples.extend([int_val] * freq)

    # Ensure total samples == shots
    if len(samples) != shots:
        # fallback: pad/truncate as necessary (shouldn't normally happen)
        samples = samples[:shots] + [0] * max(0, shots - len(samples))

    return counts, samples
