"""
main.py
Flask API server for food delivery delay prediction.
Endpoints:
  GET  /health   → Health check
  POST /predict  → Delay prediction
"""

import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ── Load model artifacts ─────────────────────────────────────────────────────
rf_model = joblib.load("rf_model.pkl")
kmeans = joblib.load("kmeans.pkl")
cluster_imputer = joblib.load("cluster_imputer.pkl")
cluster_scaler = joblib.load("cluster_scaler.pkl")

print("[OK] All model artifacts loaded successfully")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Server is running"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # ── Extract input values ──────────────────────────────────────────
        distance_km = float(data.get("Distance_km", 0))
        age = float(data.get("Delivery_person_Age", 25))
        rating = float(data.get("Delivery_person_Ratings", 4.5))
        vehicle_condition = int(data.get("Vehicle_condition", 2))
        multiple_deliveries = float(data.get("multiple_deliveries", 0))

        weather = data.get("Weather_conditions", "Sunny")
        traffic = data.get("Road_traffic_density", "Medium")
        order_type = data.get("Type_of_order", "Snack")
        vehicle_type = data.get("Type_of_vehicle", "motorcycle")
        festival = data.get("Festival", "No")
        city = data.get("City", "Delhi")

        # ── Step 1: Predict delivery cluster ──────────────────────────────
        cluster_features = np.array([[
            distance_km, age, rating, vehicle_condition, multiple_deliveries
        ]])

        cluster_imputed = cluster_imputer.transform(cluster_features)
        cluster_scaled = cluster_scaler.transform(cluster_imputed)
        delivery_cluster = str(kmeans.predict(cluster_scaled)[0])

        # ── Step 2: Build feature DataFrame ───────────────────────────────
        input_df = pd.DataFrame([{
            "Delivery_person_Age": age,
            "Delivery_person_Ratings": rating,
            "Weather_conditions": weather,
            "Road_traffic_density": traffic,
            "Vehicle_condition": vehicle_condition,
            "Type_of_order": order_type,
            "Type_of_vehicle": vehicle_type,
            "multiple_deliveries": multiple_deliveries,
            "Festival": festival,
            "City": city,
            "Distance_km": distance_km,
            "Delivery_Cluster": delivery_cluster,
        }])

        # ── Step 3: Predict ───────────────────────────────────────────────
        prediction = rf_model.predict(input_df)[0]
        probabilities = rf_model.predict_proba(input_df)[0]

        # Find probability of "Yes" (delayed)
        classes = rf_model.classes_.tolist()
        yes_index = classes.index("Yes")
        delay_probability = round(float(probabilities[yes_index]), 4)

        status = "LIKELY DELAYED" if prediction == "Yes" else "LIKELY ON TIME"

        return jsonify({
            "prediction": prediction,
            "status": status,
            "probability": delay_probability,
            "delivery_cluster": int(delivery_cluster)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
