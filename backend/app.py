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

ROUTES = [
    {
        "route_id": "R01",
        "from": "Central Bus Stand",
        "to": "Avinashi Road Terminal",
        "color": "#ff6b6b",
        "schedule": ["07:10", "08:20", "09:40", "10:55", "12:15", "14:05", "16:30", "17:50"],
    },
    {
        "route_id": "R02",
        "from": "Race Course",
        "to": "Singanallur Depot",
        "color": "#4cc9f0",
        "schedule": ["06:45", "08:00", "09:15", "11:30", "13:05", "15:25", "17:15", "18:40"],
    },
    {
        "route_id": "R03",
        "from": "Town Hall",
        "to": "Airport Link",
        "color": "#ffd166",
        "schedule": ["07:00", "08:40", "10:20", "12:05", "14:15", "16:00", "17:45", "19:10"],
    },
    {
        "route_id": "R04",
        "from": "Pillayar Koil",
        "to": "Kovaipudur Junction",
        "color": "#8ac926",
        "schedule": ["06:30", "07:50", "09:10", "11:00", "13:20", "15:10", "17:00", "18:30"],
    },
    {
        "route_id": "R05",
        "from": "Hoody",
        "to": "IIT Bus Stop",
        "color": "#ff9f1c",
        "schedule": ["06:50", "08:15", "09:50", "11:45", "13:45", "15:35", "17:30", "19:05"],
    },
    {
        "route_id": "R06",
        "from": "Kurinji Nagar",
        "to": "Thudiyalur",
        "color": "#9b5de5",
        "schedule": ["07:20", "08:35", "10:05", "12:30", "14:40", "16:20", "18:00", "19:40"],
    },
    {
        "route_id": "R07",
        "from": "Ukkadam",
        "to": "Singanallur Depot",
        "color": "#ff006e",
        "schedule": ["07:05", "08:25", "09:45", "11:15", "13:30", "15:40", "17:20", "19:00"],
    },
]

ROUTE_BUS_FLEETS = {
    "R01": ["BUS101", "BUS102", "BUS103", "BUS104", "BUS105"],
    "R02": ["BUS201", "BUS202", "BUS203", "BUS204", "BUS205"],
    "R03": ["BUS301", "BUS302", "BUS303", "BUS304", "BUS305"],
    "R04": ["BUS401", "BUS402", "BUS403", "BUS404", "BUS405"],
    "R05": ["BUS501", "BUS502", "BUS503", "BUS504", "BUS505"],
    "R06": ["BUS601", "BUS602", "BUS603", "BUS604", "BUS605"],
    "R07": ["BUS701", "BUS702", "BUS703", "BUS704", "BUS705"],
}


def _route_payload():
    result = []
    for route in ROUTES:
        route_id = route["route_id"]
        result.append({
            "route_id": route_id,
            "from": route["from"],
            "to": route["to"],
            "color": route["color"],
            "stops": ROUTE_STOPS[route_id],
            "schedule": route["schedule"],
        })
    return result

def _time_to_minutes(value):
    if value is None:
        return None
    try:
        hour, minute = map(int, str(value).split(":"))
        return hour * 60 + minute
    except (TypeError, ValueError):
        return None


def _fmt_time(minutes):
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def _normalize_stop(value):
    return " ".join(str(value).strip().lower().split())


def _find_route_for_trip(start_name, end_name):
    """
    Find the best route for the selected origin and destination.

    Priority:
    1. Direct route where both stops exist and destination comes after origin.
    2. If no direct route exists, find a route containing the destination.
       This allows the frontend to show a useful destination route instead
       of keeping the previously selected route.
    """
    start_key = _normalize_stop(start_name)
    end_key = _normalize_stop(end_name)

   
