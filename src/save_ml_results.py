import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load database settings
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Load dataset
data = pd.read_csv("data/raw/smart_home_data.csv")

# -----------------------------
# 1. ENERGY PREDICTION
# -----------------------------

energy_model = joblib.load("models/energy_model.pkl")

energy_features = [
    "temperature",
    "humidity",
    "ac_on",
    "lights_on",
    "tv_on"
]

predicted_power = energy_model.predict(data[energy_features])

# -----------------------------
# 2. ANOMALY DETECTION
# -----------------------------

anomaly_model = joblib.load("models/anomaly_model.pkl")

anomaly_features = [
    "temperature",
    "humidity",
    "ac_on",
    "lights_on",
    "tv_on",
    "power_watts"
]

anomaly_prediction = anomaly_model.predict(data[anomaly_features])

# Convert -1 / 1 into readable values
anomaly_status = [
    "ANOMALY" if value == -1 else "NORMAL"
    for value in anomaly_prediction
]

# -----------------------------
# 3. CREATE RESULTS
# -----------------------------

results = pd.DataFrame({
    "temperature": data["temperature"],
    "humidity": data["humidity"],
    "ac_on": data["ac_on"],
    "lights_on": data["lights_on"],
    "tv_on": data["tv_on"],
    "actual_power_watts": data["power_watts"],
    "predicted_power_watts": predicted_power.round(2),
    "anomaly_status": anomaly_status,
    "recorded_at": data["recorded_at"]
})

# -----------------------------
# 4. SAVE TO POSTGRESQL
# -----------------------------

results.to_sql(
    "ml_predictions",
    engine,
    if_exists="append",
    index=False
)

print("ML results saved successfully!")
print("Rows inserted:", len(results))

print("\nExample results:")
print(results.head())

print("\nDataset columns:")
print(data.columns.tolist())