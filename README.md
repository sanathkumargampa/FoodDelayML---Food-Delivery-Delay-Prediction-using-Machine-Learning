# Food Delivery Delay Predictor

AI-powered web application that predicts whether a food delivery will be delayed, using a **Random Forest Classifier** with **K-Means clustering** (93.8% accuracy).

## Tech Stack

- **Backend**: Flask (Python) — ML inference API
- **Frontend**: React.js (Vite) — Modern dark-themed UI
- **ML Models**: Random Forest + K-Means (scikit-learn)

## Quick Start

### 1. Train the Model (one-time)

```bash
cd backend
pip install -r requirements.txt
python train_model.py
```

This generates 4 `.pkl` model artifacts.

### 2. Start the Backend

```bash
cd backend
python main.py
```

Server runs at `http://localhost:5000`.

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`.

## API Endpoints

| Method | Endpoint   | Description          |
|--------|------------|----------------------|
| GET    | `/health`  | Health check         |
| POST   | `/predict` | Delay prediction     |

### Sample Request

```json
{
  "Distance_km": 15.0,
  "Delivery_person_Age": 25,
  "Delivery_person_Ratings": 4.2,
  "Vehicle_condition": 2,
  "multiple_deliveries": 2,
  "Weather_conditions": "Stormy",
  "Road_traffic_density": "Jam",
  "Type_of_order": "Meal",
  "Type_of_vehicle": "motorcycle",
  "Festival": "Yes",
  "City": "Delhi"
}
```

### Sample Response

```json
{
  "prediction": "Yes",
  "status": "LIKELY DELAYED",
  "probability": 0.82,
  "delivery_cluster": 3
}
```
