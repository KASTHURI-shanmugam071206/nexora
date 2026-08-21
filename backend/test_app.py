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

