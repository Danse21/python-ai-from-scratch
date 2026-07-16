# Create a CancerClassifier neural network using nn.Module with at least 3 layers.
# Train it on the breast cancer dataset (same data as Modul 6 Övning 6).
# Compare accuracy to your scikit-learn models from Modul 6.

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class CancerClassifier(nn.Module):
  def __init__(self, input_size: int, hidden_size: int, output_size: int):
    super().__init__()
    self.network = nn.Sequential(
      nn.Linear(input_size, hidden_size),
      nn.ReLU(),
      nn.Dropout(0.3),
      nn.Linear(hidden_size, hidden_size // 2),
      nn.ReLU(),
      nn.Linear(hidden_size // 2, output_size),
      nn.Sigmoid()
    )
  def forward(self, x):
    return self.network(x)

# Data preparation
data = load_breast_cancer()
X, y = data.data, data.target

scaler = StandardScaler()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_t = torch.FloatTensor(X_train)
X_test_t = torch.FloatTensor(X_test)
y_train_t = torch.FloatTensor(y_train).unsqueeze(1)
y_test_t = torch.FloatTensor(y_test).unsqueeze(1)

# Model, loss, optimizer
model = CancerClassifier(input_size=30, hidden_size=64, output_size=1)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train loop
epochs = 100
for epoch in range(epochs):
  model.train()                         # set to training mode
  optimizer.zero_grad()                 # clear gradients from last step
  y_pred = model(X_train_t)             # forward pass
  loss = criterion(y_pred, y_train_t)   # compute loss
  loss.backward()                       # compute gradient
  optimizer.step()                      # update weights

  if (epoch + 1) % 10 == 0:
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# Evaluation
model.eval()              # set to evaluation mode
with torch.no_grad():     # disable gradient computation
  y_pred_test = model(X_test_t)
  predicted = (y_pred_test > 0.5).float()
  accuracy = (predicted == y_test_t).float().mean()
  print(f"\n Test Accuracy: {accuracy: .3f}")


# Accuracy comparison
# The difference in accuracy is small: nn = 0.74 vs LR = 0.970 vs RF = 0.965. This is majorly because the
# dataset is relatively small and the classes are largely linearly separable.
# When to use each tool:
# Logistic Regression: fast, interpretable, strong baseline. Try this model first.
# Random Forest: handles non-linearity, gives feature importance. Use this model when LR underperforms.
# Neural Network (nn): data with complex patterns, large data, sequences, images. Use when both models above plateau.
