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
