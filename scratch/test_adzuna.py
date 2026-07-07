import unittest
from unittest.mock import patch, MagicMock
import os
import streamlit as st

secrets_path = ".streamlit/secrets.toml"
original_secrets = ""
if os.path.exists(secrets_path):
    with open(secrets_path, "r") as f:
        original_secrets = f.read()

# Write test credentials temporarily
with open(secrets_path, "w") as f:
    f.write('ADZUNA_APP_ID = "mock_id"\nADZUNA_APP_KEY = "mock_key"\n')

# Clear streamlit cached secrets if loaded
if hasattr(st, "secrets"):
    try:
        st.secrets._cache.clear()
    except Exception:
        pass

from utils.job_api import fetch_jobs

class TestAdzunaIntegration(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_jobs_scenarios(self, mock_get):
        # Sample response payload from Adzuna API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Software Engineer Intern",
                    "company": {"display_name": "Google India"},
                    "redirect_url": "https://adzuna.com/apply/1",
                    "latitude": 12.9716,
                    "longitude": 77.5946,
                    "location": {"display_name": "Bangalore, Karnataka"}
                },
                {
                    "title": "Data Analyst",
                    "company": {"display_name": "TCS"},
                    "redirect_url": "https://adzuna.com/apply/2",
                    "latitude": None,
                    "longitude": None,
                    "location": {"display_name": "Hyderabad, Telangana"}
                },
                {
                    "title": "Senior Developer",
                    "company": {"display_name": "Infosys"},
                    "redirect_url": "https://adzuna.com/apply/3",
                    "latitude": 13.0827,
                    "longitude": 80.2707,
                    "location": {"display_name": "Chennai, Tamil Nadu"}
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test Scenario 1: Developer, Bangalore, Full-Time
        # Should match "Senior Developer" (classified as Full-Time)
        jobs_full = fetch_jobs("Developer", "Bangalore", "Full-Time")
        self.assertEqual(len(jobs_full), 1)
        self.assertEqual(jobs_full[0]["company"], "Infosys")
        self.assertEqual(jobs_full[0]["job_type"], "Full-Time")
        self.assertEqual(jobs_full[0]["latitude"], 13.0827)
        self.assertEqual(jobs_full[0]["longitude"], 80.2707)
        
        # Test Scenario 2: Data Analyst, Hyderabad, Full-Time
        # Should match "Data Analyst" (classified as Full-Time, coords are None)
        jobs_analyst = fetch_jobs("Data Analyst", "Hyderabad", "Full-Time")
        self.assertEqual(len(jobs_analyst), 1)
        self.assertEqual(jobs_analyst[0]["company"], "TCS")
        self.assertEqual(jobs_analyst[0]["latitude"], None)
        self.assertEqual(jobs_analyst[0]["longitude"], None)
        
        # Test Scenario 3: Intern, Bangalore, Internship
        # Should match "Software Engineer Intern" (classified as Internship)
        jobs_intern = fetch_jobs("Intern", "Bangalore", "Internship")
        self.assertEqual(len(jobs_intern), 1)
        self.assertEqual(jobs_intern[0]["company"], "Google India")
        self.assertEqual(jobs_intern[0]["job_type"], "Internship")
        self.assertEqual(jobs_intern[0]["latitude"], 12.9716)
        
        print("Adzuna Integration Unit Tests: ALL PASSED")

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        # Restore original secrets
        with open(secrets_path, "w") as f:
            f.write(original_secrets)
