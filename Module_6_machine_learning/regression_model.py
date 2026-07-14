# Build a regression model instead of classification: predict gc_content (a continuous value)
# from [length, a_count, t_count, g_count, c_count]. Use LinearRegression and RandomForestRegressor.
# Evaluate with mean_squared_error and r2_score. What does R² tell you about model quality?

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Generate labeled data
np.random.seed(42)

def generate_sequences(n, gc_mean, gc_std, length_mean, length_std, label):
  records = []
  for _ in range(n):
    gc = np.clip(np.random.normal(gc_mean,gc_std), 0, 100)
    length = int(np.clip(np.random.normal(length_mean, length_std), 10, 200))
    gc_count = int(length * gc / 100)
    at_count = length - gc_count
    bases = ["G"] * (gc_count // 2) + ["C"] * (gc_count // 2) + ["A"] * (at_count // 2) + ["T"] * (at_count // 2)
    np.random.shuffle(bases)
    seq = "".join(bases[:length])
    records.append({
      "sequence": seq,
      "length": length,
      "gc_content": gc,
      "a_count": seq.count("A"),
      "t_count": seq.count("T"),
      "g_count": seq.count("G"),
      "c_count": seq.count("C"),
      "label": label
    })
  return records

# prokaryotes: higher GC, shorter sequences
prokaryote = generate_sequences(500, gc_mean=55, gc_std=10, length_mean=80, length_std=20, label=0)
# eukaryotes: lower GC, longer sequences
eukaryote = generate_sequences(500, gc_mean=42, gc_std=8, length_mean=120, length_std=30, label=1)
df = pd.DataFrame(prokaryote + eukaryote)
# print(df.head())
print(df["label"].value_counts())

# Features and gc_content
X = df[["length", "a_count", "t_count", "g_count", "c_count", "label"]].values
y = df["gc_content"].values

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale: transform each feature to mean=0, std=0
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train data on LinearRegression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)
y_pred_lr = model.predict(X_test_scaled)
print(f"RL Mean squared error: {mean_squared_error(y_test, y_pred_lr):.3f}, r2 score: {r2_score(y_test, y_pred_lr):.3f}")

# Train on RandomForestRegressor model (handles non-linearity naturally)
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
y_pred_rf = rf_model.predict(X_test_scaled)
print(f"RF Mean squared error: {mean_squared_error(y_test, y_pred_rf):.3f}, r2 score: {r2_score(y_test, y_pred_rf):.3f}")

# Inference of r2 about model quality
# r2 score measures how much variance in the target the model explains compared to just
# predicting the mean every time
# r2 = 1.0 -> model explains all variance, perfect predictions
# r2 = 0.0 -> model is only good at predicting the mean
# RF's r2 = 0.990 means it explains 99% of the variance in gc_content.
# LR's r2 = 0.929 means it explains 92.9%, the remaining 7.1% not captured is the non-linear portion.
