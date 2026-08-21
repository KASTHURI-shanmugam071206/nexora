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
