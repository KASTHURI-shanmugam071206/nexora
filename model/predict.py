import json
import os
import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "eta_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "feature_config.json")

_model = None
_features = None

def _load():
    global _model, _features
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
            with open(FEATURES_PATH) as f:
                _features = json.load(f)["features"]
        except Exception as e:
            print(f"[WARN] Could not load ML model ({e}). Will use fallback only.")
            _model = False  # sentinel: tried and failed
    return _model, _features
def fallback_eta(distance_to_next_stop_m: float, current_speed_kmph: float) -> float:
    """Simple physics fallback: distance / speed, in minutes."""
    safe_speed = max(current_speed_kmph, 3.0)  # avoid divide-by-near-zero
    eta_min = (distance_to_next_stop_m / 1000) / safe_speed * 60
    return round(eta_min, 2)

