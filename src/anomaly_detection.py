import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Load smart-home data
data = pd.read_csv("data/raw/smart_home_data.csv")

# Features used for anomaly detection
features = [
    "temperature",
    "humidity",
    "ac_on",
    "lights_on",
    "tv_on",
    "power_watts"
]

X = data[features]

# Create anomaly detection model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Train the model
model.fit(X)

# Predict anomalies
data["anomaly"] = model.predict(X)

# -1 = anomaly
#  1 = normal

anomalies = data[data["anomaly"] == -1]

print("Total readings:", len(data))
print("Anomalies detected:", len(anomalies))

print("\nExample anomalies:")
print(anomalies[features].head())

# Save the model
joblib.dump(model, "models/anomaly_model.pkl")

print("\nAnomaly model saved successfully!")