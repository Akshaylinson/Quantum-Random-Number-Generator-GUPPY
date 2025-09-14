# Quantum Random Number Generator (QRNG)

A compact and reproducible Quantum Random Number Generator using Qiskit and the Aer simulator.  
This project uses Hadamard gates to create superpositions and measures qubits to generate truly quantum random bits. Results are aggregated into integer values, saved to file, and visualized.

## Features
- Generate N samples of k-bit random integers (e.g., 1024 samples of 16-bit numbers).
- Save samples to `results/random_bits.txt`.
- Produce and save two plots:
  - Histogram of sampled integer values (`random_values_hist.png`)
  - Bitwise frequency plot showing fraction of 1s per bit (`bitwise_frequency.png`)
- Minimal, modular design (`circuits/random.py` and `main.py`) for easy extension.

## Requirements
- Python 3.8+ (3.10+ recommended)
- Qiskit, Qiskit-Aer, Matplotlib

Install dependencies:
```bash
python -m pip install -r requirements.txt
