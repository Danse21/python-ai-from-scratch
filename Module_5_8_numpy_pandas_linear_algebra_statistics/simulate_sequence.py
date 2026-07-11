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

# Add a new column "gc_content" and compute GC content from each sequence
df_simulated["gc_content"] = df_simulated["sequence"].apply(lambda seq: (seq.count("G") + seq.count("C")) / len(seq) * 100)

# Plot histogram
plt.hist(df_simulated["gc_content"], bins=30)
plt.xlabel("GC Content (%)")
plt.ylabel("Frequency")
plt.title("GC Content Distribution of 1000 Simulated DNA Sequences")
plt.show()

# Compute statistics and probability
mean_gc = np.mean(df_simulated["gc_content"])
std_gc = np.std(df_simulated["gc_content"])
prob_above_60 = np.sum(df_simulated["gc_content"] > 60) / len(df_simulated)

print(f"Mean: {mean_gc: .2f}%")
print(f"Std: {std_gc: .2f}%")
print(f"P(GC > 60%): {prob_above_60: .3f}")



# Övning 6
# Compute feature vectors — each vector contains [gc_content, a_count, t_count]
# for that sequence. Stack them into a matrix. Compute the correlation matrix using np.corrcoef().
# Which features are most correlated with each other and what does that tell you biologically?

df_simulated["a_count"] = df_simulated["sequence"].str.count("A")
df_simulated["t_count"] = df_simulated["sequence"].str.count("T")

feature_matrix = df_simulated[["gc_content", "a_count", "t_count"]]
corr_matrix = np.corrcoef(feature_matrix.T)    # Compute correlation matrix and transpose (T): correlate columns (features) with each other

# Read into a DataFrame
features = ["gc_content", "a_count", "t_count"]
df_corr = pd.DataFrame(corr_matrix, index=features, columns=features)
print(df_corr.round(3))

# Interpretation of each correlation
# gc_content vs a_count (-0.589): GC content has a negative correlation with number of A (A's decreases as GC'c increases)
# This implies that a fixed DNA sequence, more GC bases will leave fewer positions for A+T.
# gc_content vs t_count (-0.567): same as in gc_content vs a_count, meaning there is fewer T's than GC's with relative strong correlation.
# a_count vs t_count (-0.331) Interestingly A vs T also has a negative correlation. This implies that A' and T's compete with each other.
# When GC is low, therr are more AT positions, but within those positions, more A means less T and vice versa. The weak value (-0.337)
# shows that they partially move together (both affected by GC) but partially oppose each other.
