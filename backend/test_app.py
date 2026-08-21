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

