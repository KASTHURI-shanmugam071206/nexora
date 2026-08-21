""
MAPPY — ETA Model Training
Trains an XGBoost regressor on the synthetic bus dataset to predict
ETA (minutes) to the next stop, then saves the model + feature list.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import joblib
import json

DATA_PATH = "/home/claude/mappy_project/data/bus_eta_dataset.csv"
MODEL_PATH = "/home/claude/mappy_project/model/eta_model.joblib"
FEATURES_PATH = "/home/claude/mappy_project/model/feature_config.json"

df = pd.read_csv(DATA_PATH)

FEATURES = [
    "stop_sequence",
    "day_of_week",
    "hour_of_day",
    "is_weekend",
    "is_rush_hour",
    "current_speed_kmph",
    "distance_to_next_stop_m",
    "historical_avg_delay_min",
    "weather",
    "dwell_time_sec",
]
