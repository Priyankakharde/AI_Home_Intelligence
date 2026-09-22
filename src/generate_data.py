import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Make results reproducible
np.random.seed(42)

# Generate 1000 hourly sensor readings
n = 1000

dates = pd.date_range(
    start="2026-01-01",
    periods=n,
    freq="h"
)

temperature = np.random.normal(27, 3, n)
humidity = np.random.normal(60, 8, n)

ac_on = np.random.choice([0, 1], n, p=[0.4, 0.6])
lights_on = np.random.choice([0, 1], n, p=[0.3, 0.7])
tv_on = np.random.choice([0, 1], n, p=[0.6, 0.4])

# Simple realistic relationship:
# AC uses the most power, then TV, then lights.
power = (
    ac_on * np.random.normal(1200, 100, n)
    + lights_on * np.random.normal(12, 2, n)
    + tv_on * np.random.normal(100, 15, n)
    + np.random.normal(20, 5, n)
)

data = pd.DataFrame({
    "temperature": temperature.round(2),
    "humidity": humidity.round(2),
    "ac_on": ac_on,
    "lights_on": lights_on,
    "tv_on": tv_on,
    "power_watts": power.round(2),
    "recorded_at": dates
})

# Save locally
data.to_csv("data/raw/smart_home_data.csv", index=False)

print("Dataset created successfully!")
print("Rows:", len(data))
print(data.head())

# Store in PostgreSQL
data.to_sql(
    "ml_sensor_data",
    engine,
    if_exists="replace",
    index=False
)

print("Dataset stored in PostgreSQL!")