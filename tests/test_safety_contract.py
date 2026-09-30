import unittest

from fastapi.testclient import TestClient

from app.main import app


class SafetyContractTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_reason_does_not_change_structured_safety_request(self):
        fever = self.client.post(
            "/api/v1/safety/check",
            json={
                "medicineName": "Amoxicillin",
                "activeIngredient": "amoxicillin",
                "patientDrugAllergies": ["Penicillin"],
                "reason": "Fever",
            },
        ).json()
        headache = self.client.post(
            "/api/v1/safety/check",
            json={
                "medicineName": "Amoxicillin",
                "activeIngredient": "amoxicillin",
                "patientDrugAllergies": ["Penicillin"],
                "reason": "Headache",
            },
        ).json()

        self.assertEqual(fever, headache)

    def test_missing_model_returns_unknown_instead_of_safe(self):
        response = self.client.post(
            "/api/v1/safety/check",
            json={
                "medicineName": "Amoxicillin",
                "activeIngredient": "amoxicillin",
                "patientDrugAllergies": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["safe"])
        self.assertEqual(response.json()["prediction"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()