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
            _model = False  
    return _model, _features
    
def fallback_eta(distance_to_next_stop_m: float, current_speed_kmph: float) -> float:
    """Simple physics fallback: distance / speed, in minutes."""
    safe_speed = max(current_speed_kmph, 3.0)  
    eta_min = (distance_to_next_stop_m / 1000) / safe_speed * 60
    return round(eta_min, 2)


def predict_eta(payload: dict) -> dict:
    """
    payload keys expected (ML path):
      stop_sequence, day_of_week, hour_of_day, is_weekend, is_rush_hour,
      current_speed_kmph, distance_to_next_stop_m, historical_avg_delay_min,
      weather, dwell_time_sec

    Returns: {"eta_min": float, "source": "ml" | "fallback"}
    """
    model, features = _load()


    if model and model is not False:
        try:
            row = {feat: payload[feat] for feat in features}
            X = pd.DataFrame([row])
            eta = float(model.predict(X)[0])
            return {"eta_min": round(max(eta, 0.1), 2), "source": "ml"}
        except (KeyError, Exception) as e:
            print(f"[WARN] ML prediction failed ({e}). Falling back.")
            
    eta = fallback_eta(
        payload.get("distance_to_next_stop_m", 500),
        payload.get("current_speed_kmph", 15),
    )
    return {"eta_min": eta, "source": "fallback"}

if __name__ == "__main__":
    sample = {
        "stop_sequence": 5,
        "day_of_week": 1,
        "hour_of_day": 9,
        "is_weekend": 0,
        "is_rush_hour": 1,
        "current_speed_kmph": 14.5,
        "distance_to_next_stop_m": 1200,
        "historical_avg_delay_min": 3.2,
        "weather": 0,
        "dwell_time_sec": 40,
    }
    print("ML-path result:", predict_eta(sample))
    
    incomplete = {"distance_to_next_stop_m": 1200, "current_speed_kmph": 14.5}
    print("Fallback-only result:", predict_eta(incomplete))
