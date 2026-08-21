# MAPPY — Resilient, Inclusive Transport Solution

Starter project matching the pitch deck: an ML-powered bus ETA prediction
engine with an automatic distance/speed fallback, a Flask API, and a
map-based demo frontend.

## What's included

```
mappy_project/
├── data/
│   ├── generate_dataset.py     # generates the synthetic dataset
│   └── bus_eta_dataset.csv     # 8,000-row dataset (>= 5,000 required)
├── model/
│   ├── train_model.py          # trains the XGBoost ETA model
│   ├── predict.py              # ML prediction + fallback logic
│   ├── eta_model.joblib        # trained model (pre-built)
│   └── feature_config.json     # feature list + test MAE
├── backend/
│   └── app.py                  # Flask API: /api/health, /api/buses, /api/eta
├── frontend/
│   └── index.html              # Leaflet-based live map demo (PWA-style)
└── requirements.txt
```

## Dataset

`data/bus_eta_dataset.csv` has **8,000 rows** simulating GPS/trip records
across 6 routes and 24 buses, with realistic rush-hour, weekend, and
weather patterns. Columns:

| Column | Description |
|---|---|
| route_id, bus_id, stop_sequence | trip identifiers |
| day_of_week, hour_of_day, is_weekend, is_rush_hour | time features |
| current_speed_kmph | bus speed at time of reading |
| distance_to_next_stop_m | distance remaining to next stop |
| historical_avg_delay_min | route/time-bucket historical delay |
| weather | 0 = clear, 1 = rain, 2 = heavy rain |
| dwell_time_sec | time stopped at last stop (occupancy proxy) |
| **actual_eta_min** | target — minutes to next stop |

Regenerate or resize it any time:
```bash
python3 data/generate_dataset.py
```
Edit `N_ROWS` at the top of the script to change the row count.

## 1. Setup

```bash
pip install -r requirements.txt
```

## 2. Train the model

```bash
python3 model/train_model.py
```
Current run achieves **MAE ≈ 0.55 min** and **R² ≈ 0.96** on held-out data.
Saves `model/eta_model.joblib` + `model/feature_config.json`.

## 3. Run the backend

```bash
cd backend
python3 app.py
```
Starts on `http://localhost:5000`:
- `GET /api/health` — service check
- `GET /api/buses` — mock live GPS feed (swap for real MQTT/GPS ingestion later)
- `POST /api/eta` — ETA prediction; pass full feature set for the ML path,
  or just `distance_to_next_stop_m` + `current_speed_kmph` to force the
  fallback path.

## 4. Run the frontend

Open `frontend/index.html` directly in a browser (or serve it with any
static server). It polls `/api/buses` and `/api/eta` every few seconds and
renders live positions + ETAs on an OpenStreetMap/Leaflet map. If the
backend is unreachable, the page itself falls back to a client-side
distance/speed calculation — same resilience principle as the backend.

## Architecture recap (matches the pitch deck)

- **ML layer**: XGBoost baseline, trained on `distance`, `speed`,
  `time-of-day`, `historical delay`, etc. → `model/predict.py`
- **Resilience**: distance ÷ average-speed fallback if the model or a
  required feature is missing — never returns no ETA.
- **Backend**: Flask + CORS, ready to swap the mock `/api/buses` feed for
  a real MQTT/GPS ingestion pipeline.
- **Frontend**: OpenStreetMap + Leaflet, no paid mapping APIs, works as a
  lightweight PWA shell.
- **Future work**: LSTM+CNN spatio-temporal model, occupancy prediction,
  breakdown anomaly detection, SMS/IVR channel, GTFS-Realtime feed.

## Next steps for the hackathon

1. Swap the synthetic dataset for real/simulated GPS logs from your routes.
2. Wire `/api/buses` to actual bus GPS devices over MQTT.
3. Add the occupancy/anomaly-detection models described in the Solution slide.
4. Add SMS/IVR gateway integration for feature-phone access.
5. Publish a GTFS-Realtime feed for third-party integration.
