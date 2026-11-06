
import unittest
from app import app


class SecureAPITests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_valid_number(self):
        response = self.client.post("/double", json={"value": 25})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 50)

    def test_reject_text(self):
        response = self.client.post("/double", json={"value": "hello"})
        self.assertEqual(response.status_code, 400)

    def test_reject_boolean(self):
        response = self.client.post("/double", json={"value": True})
        self.assertEqual(response.status_code, 400)

    def test_reject_value_above_limit(self):
        response = self.client.post("/double", json={"value": 1000001})
        self.assertEqual(response.status_code, 400)

    def test_accept_positive_boundary(self):
        response = self.client.post("/double", json={"value": 1000000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 2000000)

    def test_accept_negative_boundary(self):
        response = self.client.post("/double", json={"value": -1000000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], -2000000)

    def test_reject_negative_value_below_limit(self):
        response = self.client.post("/double", json={"value": -1000001})
        self.assertEqual(response.status_code, 400)

    def test_reject_nan(self):
        response = self.client.post(
            "/double",
            data='{"value": NaN}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_reject_infinity(self):
        response = self.client.post(
            "/double",
            data='{"value": Infinity}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()

