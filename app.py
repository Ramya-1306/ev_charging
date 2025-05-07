from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import joblib
import numpy as np
import bcrypt

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.ev_charging_system
users_collection = db.users
reservations_collection = db.reservations

# Load ML Models
mileage_model = joblib.load("mileage_model.pkl")
battery_model = joblib.load("battery_model.pkl")

# Serve HTML Pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/dashboard-page")
def dashboard_page():
    return render_template("dashboard.html")

# Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name, email, password = data.get("name"), data.get("email"), data.get("password")

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users_collection.insert_one({"name": name, "email": email, "password": hashed_password})
    return jsonify({"message": "User registered successfully!"}), 201

# Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data.get("email"), data.get("password")
    
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404

    stored_hashed_password = user["password"]
    if not bcrypt.checkpw(password.encode(), stored_hashed_password):
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"message": "Login successful"}), 200

@app.route("/reserve", methods=["POST"])
def reserve_slot():
    data = request.json
    user_email = data["email"]
    station_id = data["station_id"]
    slot_number = data["slot_number"]  # User-selected slot
    date = data["date"]
    time = data["time"]

    # Check if the selected slot at the station is already booked
    existing_reservation = reservations_collection.find_one({
        "station_id": station_id,
        "slot_number": slot_number,
        "date": date,
        "time": time
    })

    if existing_reservation:
        return jsonify({"error": f"Slot {slot_number} at Station {station_id} is already reserved!"}), 400

    # Check if the user already booked a slot at the same time in the same station
    user_existing_reservation = reservations_collection.find_one({
        "email": user_email,
        "station_id": station_id,
        "date": date,
        "time": time
    })

    if user_existing_reservation:
        return jsonify({"error": "You have already reserved a slot at this station for this time!"}), 400

    # If slot is available, save the reservation
    reservations_collection.insert_one({
        "email": user_email,
        "station_id": station_id,
        "slot_number": slot_number,
        "date": date,
        "time": time
    })

    return jsonify({"message": f"Slot {slot_number} reserved successfully at Station {station_id}!"}), 201

# Predict Mileage
@app.route("/predict/mileage", methods=["POST"])
def predict_mileage():
    try:
        data = request.json
        odometer, battery_health = float(data["odometer"]), float(data["battery_health"])
        prediction = mileage_model.predict(np.array([[odometer, battery_health]]))[0]
        return jsonify({"predicted_mileage": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Predict Battery Health
@app.route("/predict/battery", methods=["POST"])
def predict_battery_health():
    try:
        data = request.json
        charging_cycles, age = float(data["charging_cycles"]), float(data["age"])
        prediction = battery_model.predict(np.array([[charging_cycles, age]]))[0]
        return jsonify({"predicted_battery_health": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
