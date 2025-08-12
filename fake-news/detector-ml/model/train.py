# model/train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import os

# Load datasets
fake = pd.read_csv('dataset/Fake.csv')
true = pd.read_csv('dataset/True.csv')

# Add labels
fake['label'] = 0  # Fake
true['label'] = 1  # Real

# Combine and shuffle
df = pd.concat([fake, true], axis=0).sample(frac=1).reset_index(drop=True)

# Split features and labels
X = df['text']
y = df['label']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
model = PassiveAggressiveClassifier(max_iter=50)
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
score = accuracy_score(y_test, y_pred)
print(f'Accuracy: {round(score * 100, 2)}%')
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save model and vectorizer
with open('model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ Model and vectorizer saved successfully.")
