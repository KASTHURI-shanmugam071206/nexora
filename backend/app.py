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
ROUTE_STOPS = {
    "R01": [
        {"lat": 11.0168, "lng": 76.9558, "name": "Central Bus Stand"},
        {"lat": 11.0200, "lng": 76.9600, "name": "Gandhipuram Junction"},
        {"lat": 11.0230, "lng": 76.9650, "name": "Brookefields Mall"},
        {"lat": 11.0260, "lng": 76.9700, "name": "Avinashi Road Terminal"},
    ],
    "R02": [
        {"lat": 11.0100, "lng": 76.9500, "name": "Race Course"},
        {"lat": 11.0140, "lng": 76.9550, "name": "Kaveri Nagar"},
        {"lat": 11.0180, "lng": 76.9590, "name": "Peelamedu Station"},
        {"lat": 11.0220, "lng": 76.9630, "name": "Singanallur Depot"},
    ],
    "R03": [
        {"lat": 11.0090, "lng": 76.9650, "name": "Town Hall"},
        {"lat": 11.0145, "lng": 76.9638, "name": "Ukkadam"},
        
{"lat": 11.0188, "lng": 76.9612, "name": "MTP Road"},
        {"lat": 11.0240, "lng": 76.9590, "name": "Airport Link"},
    ],
    "R04": [
        {"lat": 11.0305, "lng": 76.9490, "name": "Pillayar Koil"},
        {"lat": 11.0280, "lng": 76.9525, "name": "Sivananda Colony"},
        {"lat": 11.0240, "lng": 76.9580, "name": "Nehru Stadium"},
        {"lat": 11.0195, "lng": 76.9625, "name": "Kovaipudur Junction"},
    ],
    "R05": [
        {"lat": 11.0060, "lng": 76.9720, "name": "Hoody"},
        {"lat": 11.0115, "lng": 76.9688, "name": "Ramanathapuram"},
        {"lat": 11.0165, "lng": 76.9655, "name": "Saibaba Colony"},
        {"lat": 11.0210, "lng": 76.9610, "name": "IIT Bus Stop"},
    ],
    "R06": [
        {"lat": 11.0260, "lng": 76.9455, "name": "Kurinji Nagar"},
        {"lat": 11.0225, "lng": 76.9510, "name": "Vadavalli"},
        {"lat": 11.0180, "lng": 76.9555, "name": "Ranganathapuram"},
        {"lat": 11.0125, "lng": 76.9615, "name": "Thudiyalur"},
    ],
    "R07": [
        {"lat": 11.0145, "lng": 76.9638, "name": "Ukkadam"},
        {"lat": 11.0170, "lng": 76.9620, "name": "MTP Road"},
        {"lat": 11.0190, "lng": 76.9600, "name": "Peelamedu Station"},
        {"lat": 11.0220, "lng": 76.9630, "name": "Singanallur Depot"},
    ],
}

