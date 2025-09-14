# main.py
import os
import argparse
from collections import Counter
from circuits.random import run_qrng
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

def save_samples_txt(samples, out_path):
    with open(out_path, "w") as f:
        for s in samples:
            f.write(f"{s}\n")

def plot_and_save_histograms(counts, samples, num_bits, out_folder):
    os.makedirs(out_folder, exist_ok=True)

    # 1) Histogram of integer values (0 .. 2^num_bits-1) using raw counts
    fig1 = plt.figure(figsize=(6,4))
    plot_histogram(counts)
    plt.title(f"QRNG: {len(samples)} samples, {num_bits}-bit values (raw counts)")
    plt.tight_layout()
    hist1_path = os.path.join(out_folder, "random_values_hist.png")
    fig1.savefig(hist1_path)
    print(f"Saved histogram of values to: {hist1_path}")

    # 2) Bitwise frequency plot: fraction of 1s per bit position
    # Convert samples to bit arrays and count per bit index
    max_val = 2**num_bits
    bit_counts = [0] * num_bits
    for v in samples:
        for i in range(num_bits):
            # test bit i counting from LSB (i=0) to MSB (i=num_bits-1)
            if (v >> i) & 1:
                bit_counts[i] += 1
    bit_fracs = [cnt / len(samples) for cnt in bit_counts]

    fig2 = plt.figure(figsize=(6,3))
    plt.bar(range(num_bits), bit_fracs)
    plt.ylim(0,1)
    plt.xlabel("Bit index (LSB = 0)")
    plt.ylabel("Fraction of 1s")
    plt.title("Bitwise frequency (fraction of 1s per bit position)")
    plt.xticks(range(num_bits))
    plt.grid(axis='y', alpha=0.3)
    bitfreq_path = os.path.join(out_folder, "bitwise_frequency.png")
    fig2.savefig(bitfreq_path)
    print(f"Saved bitwise frequency plot to: {bitfreq_path}")

    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Quantum Random Number Generator (QRNG)")
    parser.add_argument("--bits", type=int, default=16, help="Number of bits per random number (num qubits)")
    parser.add_argument("--shots", type=int, default=1024, help="Number of samples to draw")
    parser.add_argument("--out", type=str, default="results", help="Output folder")
    args = parser.parse_args()

    num_bits = args.bits
    shots = args.shots
    out_folder = args.out

    print(f"Running QRNG: {shots} samples of {num_bits}-bit values...")
    counts, samples = run_qrng(num_bits=num_bits, shots=shots)
    print("Done. Sampled values (first 10):", samples[:10])
    print("Raw counts (top 10):", Counter(counts).most_common(10))

    os.makedirs(out_folder, exist_ok=True)
    out_txt = os.path.join(out_folder, "random_bits.txt")
    save_samples_txt(samples, out_txt)
    print(f"Saved {len(samples)} samples to {out_txt}")

    # Visualize and save histograms
    plot_and_save_histograms(counts, samples, num_bits, out_folder)

if __name__ == "__main__":
    main()

