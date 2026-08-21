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
