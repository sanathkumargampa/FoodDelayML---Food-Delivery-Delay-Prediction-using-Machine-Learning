"""
train_model.py
Replicates the ML pipeline from training.ipynb.
Run once to generate .pkl model artifacts.
"""

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ── 1. Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv("dataset.csv")
print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")


# ── 2. Data Cleaning ─────────────────────────────────────────────────────────

# Assign random Indian cities (reproducible with seed)
cities = [
    "Delhi", "Bangalore", "Hyderabad", "Pune", "Chennai",
    "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Indore",
    "Surat", "Coimbatore", "Chandigarh", "Kochi"
]
np.random.seed(42)
df["City"] = np.random.choice(cities, size=len(df))

# Fill missing values (same as notebook)
df[["Delivery_person_Age", "Delivery_person_Ratings", "multiple_deliveries"]] = (
    df[["Delivery_person_Age", "Delivery_person_Ratings", "multiple_deliveries"]].fillna(0)
)
df[["Weather_conditions", "Road_traffic_density", "Festival"]] = (
    df[["Weather_conditions", "Road_traffic_density", "Festival"]].fillna("Unknown")
)


# ── 3. Feature Engineering ───────────────────────────────────────────────────

# Haversine distance (vectorised)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

df["Distance_km"] = haversine_distance(
    df["Restaurant_latitude"],
    df["Restaurant_longitude"],
    df["Delivery_location_latitude"],
    df["Delivery_location_longitude"]
)

# Binary target
df["Delayed"] = np.where(df["Time_taken (min)"] > 30, "Yes", "No")
print(f"Target distribution:\n{df['Delayed'].value_counts().to_string()}")


# ── 4. Prepare Features ──────────────────────────────────────────────────────

drop_columns = [
    "ID", "Delivery_person_ID",
    "Restaurant_latitude", "Restaurant_longitude",
    "Delivery_location_latitude", "Delivery_location_longitude",
    "Order_Date", "Time_Orderd", "Time_Order_picked",
    "Time_taken (min)", "Delayed"
]

X = df.drop(columns=drop_columns)
y = df["Delayed"]


# ── 5. K-Means Clustering ────────────────────────────────────────────────────

cluster_features = [
    "Distance_km",
    "Delivery_person_Age",
    "Delivery_person_Ratings",
    "Vehicle_condition",
    "multiple_deliveries"
]

X_cluster = X[cluster_features].copy()

# Impute → Scale → KMeans
cluster_imputer = SimpleImputer(strategy="median")
X_cluster_imputed = cluster_imputer.fit_transform(X_cluster)

cluster_scaler = StandardScaler()
X_cluster_scaled = cluster_scaler.fit_transform(X_cluster_imputed)

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Delivery_Cluster"] = kmeans.fit_predict(X_cluster_scaled)

# Add cluster as categorical string feature
X["Delivery_Cluster"] = df["Delivery_Cluster"].astype(str)

print(f"Cluster distribution:\n{df['Delivery_Cluster'].value_counts().to_string()}")


# ── 6. Build Preprocessing + Classifier Pipeline ─────────────────────────────

numerical_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

print(f"\nNumerical features ({len(numerical_features)}): {numerical_features}")
print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numerical", numeric_pipeline, numerical_features),
    ("categorical", categorical_pipeline, categorical_features)
])

rf_model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    ))
])


# ── 7. Train / Test Split & Fit ──────────────────────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nTraining: {X_train.shape}, Testing: {X_test.shape}")

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n[OK] Test Accuracy: {accuracy:.4f}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")


# ── 8. Save Model Artifacts ──────────────────────────────────────────────────

joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(kmeans, "kmeans.pkl")
joblib.dump(cluster_imputer, "cluster_imputer.pkl")
joblib.dump(cluster_scaler, "cluster_scaler.pkl")

print("\n[OK] Saved artifacts:")
print("  - rf_model.pkl")
print("  - kmeans.pkl")
print("  - cluster_imputer.pkl")
print("  - cluster_scaler.pkl")
print("\nTraining complete!")
