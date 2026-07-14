# Build a complete MLPipeline class with methods: load_data(), preprocess(),
# train(model_name: str), evaluate(), get_feature_importance().
# It should support at least two model types selectable by name.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class MLPipeline:
  def __init__(self, model_name: str = "logistic"):
    self.model_name = model_name
    if model_name == "logistic":
      self.model = LogisticRegression(random_state=42)
    elif model_name == "random_forest":
      self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
      raise ValueError(f"Unknown model: {model_name}")

  def load_data(self):
    self.data = load_breast_cancer()
    self.X = self.data.data
    self.y = self.data.target
    self.feature_names = self.data.feature_names

  def preprocess(self):
    self.scaler = StandardScaler()
    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
    self.X_train_scaled = self.scaler.fit_transform(self.X_train)
    self.X_test_scaled = self.scaler.transform(self.X_test)

  def train(self):
    self.model.fit(self.X_train_scaled, self.y_train)
    self.y_pred = self.model.predict(self.X_test_scaled)

  def evaluate(self):
    accuracy = accuracy_score(self.y_test, self.y_pred)
    report = classification_report(self.y_test, self.y_pred, target_names=["Benign", "Malignant"])
    return accuracy, report

  def get_feature_importance(self):
    if not hasattr(self.model, "feature_importances_"):
      print("Feature importance not available for this model.")
      return
    importances = self.model.feature_importances_
    for name, importance in sorted(zip(self.feature_names, importances),
                                        key=lambda x: x[1], reverse=True):
      print(f"{name}: {importance:.3f}")

if __name__ == "__main__":
  pipeline = MLPipeline(model_name="random_forest")
  pipeline.load_data()
  pipeline.preprocess()
  pipeline.train()
  accuracy, report = pipeline.evaluate()
  print(f"Accuracy: {accuracy:.3f}")
  print(report)
  pipeline.get_feature_importance()
