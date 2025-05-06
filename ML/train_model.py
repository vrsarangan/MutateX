import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# ========== CONFIG ==========
csv_path = r"C:\Users\User\Documents\MutateX\ML\behavior_logs.csv"
model_path = os.path.join(os.path.dirname(csv_path), "malware_detector_model.pkl")

# Ensure CSV directory exists
os.makedirs(os.path.dirname(csv_path), exist_ok=True)

# Define column names
columns = [
    'Timestamp', 'CPU_Usage', 'Memory_Usage', 'Processes_Spawned',
    'Files_Created', 'Files_Deleted', 'Files_Modified', 'Packets_Captured',
    'Active_Connections', 'New_Processes_Spawned', 'label'
]

# Load the dataset
data = pd.read_csv(csv_path, header=None, names=columns)

# Check if the label column exists
label_column = 'label'
if label_column not in data.columns:
    raise ValueError(f"The dataset must contain a '{label_column}' column.")

# Selecting relevant features
features = [
    'CPU_Usage', 'Memory_Usage', 'Processes_Spawned', 'Files_Created', 
    'Files_Deleted', 'Files_Modified', 'Packets_Captured', 'Active_Connections', 
    'New_Processes_Spawned'
]
X = data[features]
y = data[label_column]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Model Accuracy: {accuracy * 100:.2f}%')

# Save model
joblib.dump(model, model_path)
print(f"Model saved to: {model_path}")
