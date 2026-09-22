import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/energy_model.pkl")

# New smart-home conditions
new_data = pd.DataFrame({
    "temperature": [30],
    "humidity": [65],
    "ac_on": [1],
    "lights_on": [1],
    "tv_on": [1]
})

# Predict power consumption
prediction = model.predict(new_data)

print("Predicted power consumption:", round(prediction[0], 2), "watts")