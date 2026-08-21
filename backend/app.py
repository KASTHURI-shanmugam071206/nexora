"""
MAPPY — Backend API
Flask server exposing:
  GET  /                     -> frontend app shell
  POST /api/login            -> demo login for local session persistence
  GET  /api/routes           -> route definitions with from/to/timing map
  GET  /api/buses            -> buses within the selected time window (+/- 15 min)
  GET  /api/health           -> service status
  POST /api/eta              -> ETA prediction (ML with automatic fallback)

Run: python app.py
Then open http://localhost:5000 in a browser.
"""

import os
import random
import sys
import time
from datetime import datetime

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

MODEL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "model")
)

sys.path.insert(0, MODEL_DIR)

from predict import predict_eta  # noqa: E402

app = Flask(__name__)
CORS(app)

USERS = {
    "demo": {"password": "pass123", "name": "Demo User"},
    "admin": {"password": "admin123", "name": "Admin User"},
}
