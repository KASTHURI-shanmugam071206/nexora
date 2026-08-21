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

TARGET = "actual_eta_min"

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=42,
    objective="reg:squarederror",
)

model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)
