# Run the full pipeline above: generate data, split, scale, train Logistic Regression,
# print accuracy and classification report. Then train a Random Forest on the same data and
# compare accuracy. Which performs better?

# DNA sequence classification prediction: Is the sequence from prokaryotes (E.coli) or eukaryotes (H. sapiens)?

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Generate labeled data
np.random.seed(42)

def generate_sequences(n, gc_mean, gc_std, length_mean, length_std, label):
  records = []
  for _ in range(n):
    gc = np.clip(np.random.normal(gc_mean, gc_std), 0, 100)
    length = int(np.clip(np.random.normal(length_mean, length_std), 10, 200))
    gc_count = int(length * gc / 100)
    at_count = length - gc_count
    bases = ["G"] * (gc_count // 2) + ["C"] * (gc_count // 2) + ["A"] * (at_count // 2) + ["T"] * (at_count // 2)
    np.random.shuffle(bases)
    seq = "".join(bases[:length])
    records.append({
      "sequence" : seq,
      "length": length,
      "gc_content": gc,
      "a_count": seq.count("A"),
      "t_count": seq.count("T"),
      "g_count": seq.count("G"),
      "c_count": seq.count("C"),
      "label": label
    })
  return records
# Prokaryotes: higher GC, shorter sequences
prokaryote = generate_sequences(500, gc_mean=55, gc_std=10, length_mean=80, length_std=20, label=0)
# Eukaryotes: lower GC, longer sequences
eukaryote = generate_sequences(500, gc_mean=42, gc_std=8, length_mean=120, length_std=30, label=1)
df = pd.DataFrame(prokaryote + eukaryote)
# print(df.head())
print(df["label"].value_counts())

# Features and labels
# Features: what the model learns from
X = df[["length", "gc_content", "a_count", "t_count", "g_count", "c_count"]]. values
# Labels: whats we're predicting (0 = prokaryote, 1 = eukaryote)
y = df["label"].values

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.2, random_state=42
)
# Dataset split: 80% for training and 20% for testing
# print(f"Training set: {X_train.shape}, Testing set: {X_test.shape}")

# Scale i.e., transform each feature to mean=0, std=0, creates consistent scale for logistic regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression. Logistic Regresssion is good for binary classification
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

# Print accuracy and classification report
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred, target_names=["prokaryote", "Eukaryote"]))

# Train same data on Random Forest and compare accuracy
# NB: Logistic Regression offers linear boundary, fast, interpretable, and is good for baseline
# whereas Random Forest comes with ensemble of decision trees, handles non-linear patterns, and is robust

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_scaled, y_train)
print(f"Random Forest Accuracy: {rf_model.score(X_test_scaled, y_test):.3f}")

# Based on printed result, Logistic Regression is slightly more accurate with a value of 0.835 as against 0.805 for Random Forest.


# Övning 2
# Print feature importances from your Random Forest. Which feature is most predictive of
# prokaryote vs eukaryote? Does that match your biological intuition?

features_names = ["length", "gc_content", "a_count", "t_count", "g_count", "c_count"]
importances = rf_model.feature_importances_

for name, importance in sorted(zip(features_names, importances),
                               key=lambda x: x[1], reverse=True):
  print(f"{name}: {importance:.3f}")

# The most predictive feature is the number of T followed by the number of A in the
# DNA sequence. Since we defined from start that prokaryotic sequences will have
# higher GC content compare to eukaryotic sequences, it matches to see that AT content
# are the top two predictive features. High GC content in prokaryotes means low AT,
# so A count and T count are mirror image of GC content.
