# Simulate 1000 random DNA sequences of length 50 using np.random.choice(["A","C","G","T"]).
# For each sequence compute GC content. Plot a histogram of GC content distribution using matplotlib.
# Compute the mean, std, and the probability that a random sequence has GC content above 60%.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dna_simulated = np.random.choice(["A", "C", "G", "T"], size=(1000, 50))

# Convert simulated dna sequences into Pandas DataFrame: row = 1000, column = 50
sequences = ["".join(row) for row in dna_simulated]
df_simulated = pd.DataFrame({
  "sample_id": [f"S{i}" for i in range(1, 1001)],
  "sequence": sequences
  })

# Compute GC content
df_simulated["gc_content"] = df_simulated["sequence"].apply(lambda seq: (seq.count("G") + seq.count("C")) / len(seq) * 100)

# Plot histogram
plt.hist(df_simulated["gc_content"], bins=30)
plt.xlabel("GC Content (%)")
plt.ylabel("Frequency")
plt.title("GC Content Distribution - 1000 Simulated Sequences")
plt.show()

# Compute statistics and probability
mean_gc = np.mean(df_simulated["gc_content"])
std_gc = np.std(df_simulated["gc_content"])
prob_above_60 = np.sum(df_simulated["gc_content"] > 60) / len(df_simulated)

print(f"Mean: {mean_gc: .2f}%")
print(f"Std: {std_gc: .2f}%")
print(f"P(GC > 60%): {prob_above_60: .3f}")
