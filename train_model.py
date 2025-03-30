# Train the model with OneHotEncoding
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,fbeta_score
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt  # Ensure matplotlib is imported
from sklearn.metrics import classification_report

# Load cleaned dataset

# Define features and target
df = pd.read_csv("cyvu_file(1).csv")

# Define features and target
X = df.drop(columns=["Disease"])  # Features (all columns except disease)
y = df["Disease"]                # Target (just the disease column)
 

# One-hot encode symptoms
#encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
#X_encoded = encoder.fit_transform(dataset[X])  # Use 'dataset' instead of 'df'

# Get feature names for the encoded columns
#encoded_feature_names = encoder.get_feature_names_out(X)
#X = pd.DataFrame(X_encoded, columns=encoded_feature_names)

# Target variable
  # Use 'dataset' here as well

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=1,
    stratify=y  # Preserve class distribution
)

# Create Decision Tree classifier object
model = DecisionTreeClassifier(
    max_depth=9,
    random_state=1,
    min_samples_split=5  # Prevents overfitting
)

# Train Decision Tree Classifier
model.fit(X_train, y_train)

# Predict the response for test dataset
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
precision = precision_score(y_test, y_pred, average='weighted')  # Changed from 'binary'
recall = recall_score(y_test, y_pred, average='weighted')       # Changed from 'binary'
f3 = fbeta_score(y_test, y_pred, beta=3, average='weighted')   # Fixed y_true to y_test

print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F3-score: {f3:.2f}")

# Print classification report for detailed metrics
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
# Visualize the decision tree with CORRECT feature names
plt.figure(figsize=(15,10))
tree.plot_tree(model, 
               feature_names=X.columns.tolist(),  # Use encoded feature names
               class_names=y.unique(), 
               filled=True)
plt.show()
#save model
import joblib


# 1. Save the trained model
joblib.dump(model, 'disease_decision_tree_model4.pkl')  # Model file

# 2. Save the OneHotEncoder (if uncommented later)
# joblib.dump(encoder, 'symptom_encoder.pkl')  

# 3. Save feature names (critical for prediction)
with open('model_feature_names.txt', 'w') as f:
    f.write('\n'.join(X.columns.tolist()))  # Save symptom category order

# 4. Save visualization (optional)
plt.figure(figsize=(15,10))
tree.plot_tree(model, 
               feature_names=X.columns.tolist(),
               class_names=y.unique(), 
               filled=True)
plt.savefig('decision_tree_visualization.png', dpi=300, bbox_inches='tight')
plt.close()