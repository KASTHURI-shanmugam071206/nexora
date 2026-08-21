"""
MAPPY — Synthetic Bus ETA Dataset Generator
Generates a realistic dataset for training the XGBoost ETA prediction model.
Simulates GPS/trip data across multiple routes, buses, and stops in a
Village  style transit network, with rush-hour and weekday/weekend patterns.
"""
import numpy as np
import pandas as pd
np.random.seed(42)
N_ROWS = 8000
N_ROUTES = 10
STOPS_PER_ROUTE = 12
N_BUSES = 45
routes = [f"R{str(i+1).zfill(2)}" for i in range(N_ROUTES)]
buses = [f"BUS{str(i+1).zfill(3)}" for i in range(N_BUSES)]
rows = []
for _ in range(N_ROWS):
    route_id = np.random.choice(routes)
    bus_id = np.random.choice(buses)
    stop_seq = np.random.randint(1, STOPS_PER_ROUTE + 1)
    day_of_week = np.random.randint(0, 7)          # 0=Mon ... 6=Sun
    hour = np.random.randint(5, 23)                # service hours 5am-11pm
    is_weekend = 1 if day_of_week >= 5 else 0
    # Rush hour flag: 8-10am and 5-8pm on weekdays
    is_rush_hour = 1 if (not is_weekend and (8 <= hour <= 10 or 17 <= hour <= 20)) else 0
    # Distance to next stop (meters) — varies by route density
    distance_to_next_stop = np.round(np.random.uniform(200, 3500), 1)
    # Base speed depends on rush hour / weekend
    if is_rush_hour:
        base_speed = np.random.normal(14, 4)   # slower in traffic
    elif is_weekend:
        base_speed = np.random.normal(28, 5)   # faster, less traffic
    else:
        base_speed = np.random.normal(22, 5)
    current_speed_kmph = np.clip(base_speed, 3, 45)
    current_speed_kmph = np.round(current_speed_kmph, 1)
    # Historical average delay (minutes) for this route/hour bucket
    hist_base = 1.5 + (3.5 if is_rush_hour else 0) + np.random.normal(0, 0.8)
    historical_avg_delay_min = np.round(np.clip(hist_base, 0, 12), 2)

print(df.describe(include="all").T[["count", "mean", "min", "max"]])
