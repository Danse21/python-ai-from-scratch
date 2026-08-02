# Create a NumPy array of 10 GC content values (mix of realistic values between 0–100).
# Compute mean, median, std, min, max. Then use boolean indexing to filter values above the mean.
# Print all results.

import numpy as np

gc_content = np.array([50.0, 62.47, 100.0, 30.0, 23.34, 40.20, 85.23, 48.5, 55.10, 72.5])

mean_value = np.mean(gc_content)
above_mean = gc_content[gc_content > mean_value]

print(f"Mean: {mean_value: .2f}")
print(f"Median: {np.median(gc_content): .2f}")
print(f"Std: {np.std(gc_content): .2f}")
print(f"Min: {np.min(gc_content): .2f}")
print(f"Max: {np.max(gc_content): .2f}")

print(f"Values above mean: {above_mean}")
