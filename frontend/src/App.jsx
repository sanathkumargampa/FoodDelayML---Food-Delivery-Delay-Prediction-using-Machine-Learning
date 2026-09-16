import { useState } from "react";
import { predictDelay } from "./api";
import "./App.css";

const CITIES = [
  "Delhi","Bangalore","Hyderabad","Pune","Chennai","Kolkata",
  "Ahmedabad","Jaipur","Lucknow","Indore","Surat","Coimbatore",
  "Chandigarh","Kochi"
];

const WEATHER = ["Sunny","Cloudy","Fog","Sandstorms","Stormy","Windy"];
const TRAFFIC = ["Low","Medium","High","Jam"];
const ORDER_TYPES = ["Snack","Meal","Drinks","Buffet"];
const VEHICLES = ["motorcycle","scooter","electric_scooter","bicycle"];
const VEHICLE_LABELS = { motorcycle:"Motorcycle", scooter:"Scooter", electric_scooter:"Electric Scooter", bicycle:"Bicycle" };
const CONDITION_LABELS = ["0 - Poor","1 - Average","2 - Good","3 - Excellent"];

const DEFAULT = {
  Delivery_person_Age: "",
  Delivery_person_Ratings: "",
  Distance_km: "",
  Vehicle_condition: "",
  multiple_deliveries: "",
  Type_of_order: "",
  Type_of_vehicle: "",
  City: "",
  Festival: "",
  Weather_conditions: "",
  Road_traffic_density: "",
};

export default function App() {
  const [form, setForm] = useState(DEFAULT);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const update = (key, val) => setForm(prev => ({ ...prev, [key]: val }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await predictDelay({
        ...form,
        Delivery_person_Age: parseFloat(form.Delivery_person_Age),
        Delivery_person_Ratings: parseFloat(form.Delivery_person_Ratings),
        Distance_km: parseFloat(form.Distance_km),
        Vehicle_condition: parseInt(form.Vehicle_condition),
        multiple_deliveries: parseFloat(form.multiple_deliveries),
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const pct = result ? Math.round(result.probability * 100) : 0;
  const isDelayed = result?.prediction === "Yes";

  return (
    <div className="app">
      <header className="header">
        <div className="header-glow" />
        <h1>Food Delivery Delay Prediction using Machine Learning</h1>
      </header>

      <main className="main">
        <form className="form-card" onSubmit={handleSubmit}>
          {/* Delivery Info */}
          <section className="form-section">
            <h2 className="section-title">Delivery Information</h2>
            <div className="form-grid">
              <label className="field">
                <span className="field-label">Person Age</span>
                <input
                  type="number"
                  min="18"
                  max="60"
                  placeholder="e.g. 29 (18-60)"
                  value={form.Delivery_person_Age}
                  onChange={e => update("Delivery_person_Age", e.target.value)}
                  required
                />
              </label>
              <label className="field">
                <span className="field-label">Person Rating</span>
                <input
                  type="number"
                  min="1"
                  max="5"
                  step="0.1"
                  placeholder="e.g. 4.6 (1-5)"
                  value={form.Delivery_person_Ratings}
                  onChange={e => update("Delivery_person_Ratings", e.target.value)}
                  required
                />
              </label>
              <label className="field">
                <span className="field-label">Distance (km)</span>
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  placeholder="e.g. 8.5"
                  value={form.Distance_km}
                  onChange={e => update("Distance_km", e.target.value)}
                  required
                />
              </label>
              <label className="field">
                <span className="field-label">Vehicle Condition</span>
                <select
                  value={form.Vehicle_condition}
                  onChange={e => update("Vehicle_condition", e.target.value)}
                  required
                >
                  <option value="" disabled>Select vehicle condition</option>
                  {CONDITION_LABELS.map((l, i) => <option key={i} value={i}>{l}</option>)}
                </select>
              </label>
              <label className="field">
                <span className="field-label">Multiple Deliveries</span>
                <select
                  value={form.multiple_deliveries}
                  onChange={e => update("multiple_deliveries", e.target.value)}
                  required
                >
                  <option value="" disabled>Select deliveries count</option>
                  {[0,1,2,3].map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              </label>
            </div>
          </section>

          {/* Order Info */}
          <section className="form-section">
            <h2 className="section-title">Order Information</h2>
            <div className="form-grid">
              <label className="field">
                <span className="field-label">Type of Order</span>
                <select
                  value={form.Type_of_order}
                  onChange={e => update("Type_of_order", e.target.value)}
                  required
                >
                  <option value="" disabled>Select order type</option>
                  {ORDER_TYPES.map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              </label>
              <label className="field">
                <span className="field-label">Type of Vehicle</span>
                <select
                  value={form.Type_of_vehicle}
                  onChange={e => update("Type_of_vehicle", e.target.value)}
                  required
                >
                  <option value="" disabled>Select vehicle type</option>
                  {VEHICLES.map(v => <option key={v} value={v}>{VEHICLE_LABELS[v]}</option>)}
                </select>
              </label>
              <label className="field">
                <span className="field-label">City</span>
                <select
                  value={form.City}
                  onChange={e => update("City", e.target.value)}
                  required
                >
                  <option value="" disabled>Select city</option>
                  {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </label>
              <label className="field">
                <span className="field-label">Festival</span>
                <select
                  value={form.Festival}
                  onChange={e => update("Festival", e.target.value)}
                  required
                >
                  <option value="" disabled>Select festival status</option>
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </label>
            </div>
          </section>

          {/* Conditions */}
          <section className="form-section">
            <h2 className="section-title">Conditions</h2>
            <div className="form-grid">
              <label className="field">
                <span className="field-label">Weather</span>
                <select
                  value={form.Weather_conditions}
                  onChange={e => update("Weather_conditions", e.target.value)}
                  required
                >
                  <option value="" disabled>Select weather condition</option>
                  {WEATHER.map(w => <option key={w} value={w}>{w}</option>)}
                </select>
              </label>
              <label className="field">
                <span className="field-label">Road Traffic Density</span>
                <select
                  value={form.Road_traffic_density}
                  onChange={e => update("Road_traffic_density", e.target.value)}
                  required
                >
                  <option value="" disabled>Select traffic density</option>
                  {TRAFFIC.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </label>
            </div>
          </section>

          <button className="submit-btn" type="submit" disabled={loading}>
            {loading ? (
              <span className="spinner" />
            ) : (
              <>Predict Delay</>
            )}
          </button>
        </form>

        {/* Error */}
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className={`result-card ${isDelayed ? "delayed" : "ontime"}`}>
            <div className="result-status">
              <span className={`status-badge ${isDelayed ? "badge-delayed" : "badge-ontime"}`}>
                {result.status}
              </span>
            </div>

            <div className="result-body">
              <div className="prob-ring-container">
                <svg className="prob-ring" viewBox="0 0 120 120">
                  <circle className="ring-bg" cx="60" cy="60" r="52" />
                  <circle
                    className={`ring-fill ${isDelayed ? "ring-delayed" : "ring-ontime"}`}
                    cx="60" cy="60" r="52"
                    strokeDasharray={`${pct * 3.267} 326.7`}
                    strokeDashoffset="0"
                  />
                </svg>
                <div className="prob-text">
                  <span className="prob-value">{pct}%</span>
                  <span className="prob-label">Delay</span>
                </div>
              </div>

              <div className="result-details">
                <div className="detail-row">
                  <span className="detail-label">Prediction</span>
                  <span className="detail-value">{isDelayed ? "Delayed" : "On Time"}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Probability</span>
                  <span className="detail-value">{(result.probability * 100).toFixed(1)}%</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Delivery Cluster</span>
                  <span className="cluster-badge">Cluster #{result.delivery_cluster}</span>
                </div>
              </div>
            </div>

            <div className="risk-factors">
              <h3>Key Risk Factors</h3>
              <div className="factor-chips">
                {form.Road_traffic_density === "Jam" && <span className="chip chip-high">Traffic Jam</span>}
                {form.Road_traffic_density === "High" && <span className="chip chip-med">High Traffic</span>}
                {(form.Weather_conditions === "Stormy" || form.Weather_conditions === "Fog" || form.Weather_conditions === "Sandstorms") && (
                  <span className="chip chip-high">{form.Weather_conditions} Weather</span>
                )}
                {form.Festival === "Yes" && <span className="chip chip-med">Festival Day</span>}
                {parseFloat(form.Distance_km) > 15 && <span className="chip chip-med">Long Distance</span>}
                {parseFloat(form.Delivery_person_Ratings) < 4.0 && <span className="chip chip-low">Low Rating</span>}
                {parseInt(form.multiple_deliveries) >= 2 && <span className="chip chip-low">Multiple Deliveries</span>}
                {form.Road_traffic_density === "Low" && form.Weather_conditions === "Sunny" && (
                  <span className="chip chip-good">Favorable Conditions</span>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

    </div>
  );
}
