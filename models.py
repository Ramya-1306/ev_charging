import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Training Data
data = {
    "odometer": [5000, 10000, 15000, 20000, 25000],
    "battery_health": [90, 85, 80, 75, 70],
    "charging_cycles": [100, 200, 300, 400, 500],
    "age": [1, 2, 3, 4, 5],
    "mileage": [300, 290, 280, 270, 260]
}

df = pd.DataFrame(data)

# Train Models
mileage_model = LinearRegression().fit(df[["odometer", "battery_health"]], df["mileage"])
battery_model = LinearRegression().fit(df[["charging_cycles", "age"]], df["battery_health"])

# Save Models
joblib.dump(mileage_model, "mileage_model.pkl")
joblib.dump(battery_model, "battery_model.pkl")
