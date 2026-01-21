from sklearn.linear_model import LogisticRegression
import numpy as np
import pickle

# 1. Generate some example data
X = np.random.rand(100, 3)  # 100 rows, 3 features
y = (X.sum(axis=1) > 1.5).astype(int)  # simple target: 1 if sum > 1.5 else 0

# 2. Train a model
model = LogisticRegression()
model.fit(X, y)

# 3. Save the model properly as a binary pickle
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")
