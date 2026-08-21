import json
import unittest
from app import app

class AppApiTests(unittest.TestCase):
  def test_login_endpoint_accepts_demo_user(self):
        client = app.test_client()
        response = client.post(
            "/api/login",
            data=json.dumps({"username": "demo", "password": "pass123"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload["success"])
        self.assertEqual(payload["user"], "demo")

   
  def test_routes_endpoint_returns_schedule_and_route_details(self):
        client = app.test_client()
        response = client.get("/api/routes")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, list)
        self.assertGreaterEqual(len(payload), 2)
        route = payload[0]
        self.assertIn("route_id", route)
        self.assertIn("from", route)
        self.assertIn("to", route)
        self.assertIn("schedule", route)
        self.assertIn("color", route)

   def test_routes_endpoint_includes_all_dataset_routes(self):
        client = app.test_client()
        response = client.get("/api/routes")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        route_ids = {route["route_id"] for route in payload}
        self.assertTrue({"R01", "R02", "R03", "R04", "R05", "R06"}.issubset(route_ids))

   def test_buses_endpoint_includes_at_least_five_buses_per_route(self):
        client = app.test_client()
        response = client.get("/api/buses?route_id=R01&time=09:30")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertGreaterEqual(len(payload), 5)
        self.assertTrue(all(item["route_id"] == "R01" for item in payload))

    def test_route_search_matches_user_from_and_destination(self):
        client = app.test_client()
        response = client.get("/api/route-search?from=Central%20Bus%20Stand&to=Avinashi%20Road%20Terminal&time=09:30")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["route_id"], "R01")
        self.assertEqual(payload["from"], "Central Bus Stand")
        self.assertEqual(payload["to"], "Avinashi Road Terminal")
        self.assertGreaterEqual(len(payload["buses"]), 5)

if __name__ == "__main__":
    unittest.main()

   
