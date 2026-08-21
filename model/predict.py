import json
import os
import joblib
import pandas as pd


MODEL_PATH = os.path.join(os.path.dirname(__file__), "eta_model.joblib")
FEATURES_PATH = os.path.join(os.path.dirname(__file__), "feature_config.json")


_model = None
_features = None
