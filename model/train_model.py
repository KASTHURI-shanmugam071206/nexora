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
