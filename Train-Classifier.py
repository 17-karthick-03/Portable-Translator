import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load Data
with open('path/to/the/directory/data.pickle', 'rb') as f:
    data_dict = pickle.load(f)

data = data_dict['data']
labels = data_dict['labels']

# ✅ Find max length of feature vectors
max_length = max(len(d) for d in data)

# ✅ Pad all feature vectors to have the same length
data_padded = [d + [0] * (max_length - len(d)) for d in data]

# ✅ Convert to NumPy array
data = np.array(data_padded)
labels = np.array(labels)

# Split Data
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Train Model
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Predict
y_predict = model.predict(x_test)
score = accuracy_score(y_test, y_predict)

print(f"{score * 100:.2f}% of samples were classified correctly!")

# Save Model
with open('/home/karthick/Downloads/ISL_Working/model.p', 'wb') as f:
    pickle.dump({'model': model}, f)

print("✅ Model saved as 'model.p'")
