import os
import pandas as pd
import unittest
from datetime import datetime

# Setup mock streamlit session state
import streamlit as st
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

from utils.session_manager import load_profiles, save_profile

class TestLoginPersistence(unittest.TestCase):
    
    def setUp(self):
        # Ensure clean directories
        if not os.path.exists("data/users"):
            os.makedirs("data/users", exist_ok=True)
            
    def test_flow_durga_user(self):
        email = "durga@gmail.com"
        name = "Durga Prasad"
        safe_email = email.replace("@", "_").replace(".", "_")
        user_file = f"data/users/{safe_email}.csv"
        
        # 1. First-time registration
        if os.path.exists(user_file):
            os.remove(user_file)
            
        save_profile(email, name)
        profiles = load_profiles()
        self.assertIn(email, profiles)
        self.assertEqual(profiles[email]["name"], name)
        
        # Create user CSV file
        columns = [
            "Date", "Topic", "ProblemsSolved", "MockScore", 
            "Applications", "ProjectCount", "StudyHours"
        ]
        df_empty = pd.DataFrame(columns=columns)
        df_empty.to_csv(user_file, index=False)
        self.assertTrue(os.path.exists(user_file))
        
        # 2. Add progress entry
        df = pd.read_csv(user_file)
        new_row = pd.DataFrame([{
            "Date": "2026-06-16",
            "Topic": "Dynamic Programming",
            "ProblemsSolved": 5,
            "MockScore": 85.0,
            "Applications": 2,
            "ProjectCount": 1,
            "StudyHours": 4.5
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(user_file, index=False)
        
        # Verify file has 1 row
        df_loaded = pd.read_csv(user_file)
        self.assertEqual(len(df_loaded), 1)
        self.assertEqual(df_loaded.iloc[0]["Topic"], "Dynamic Programming")
        
        # 3. Simulate returning user log in
        profiles_loaded = load_profiles()
        self.assertIn(email, profiles_loaded)
        user_meta = profiles_loaded.get(email) or {}
        self.assertEqual(user_meta.get("name"), "Durga Prasad")
        
        df_restored = pd.read_csv(user_file)
        self.assertEqual(len(df_restored), 1)
        print("Test Case 1 (Durga Prasad) - Persistent Save & Restore: PASSED")
        
    def test_flow_test_user(self):
        # Test Case 2: Verify separate dataset for test@gmail.com
        email = "test@gmail.com"
        name = "Test User"
        safe_email = email.replace("@", "_").replace(".", "_")
        user_file = f"data/users/{safe_email}.csv"
        
        if os.path.exists(user_file):
            os.remove(user_file)
            
        save_profile(email, name)
        
        columns = [
            "Date", "Topic", "ProblemsSolved", "MockScore", 
            "Applications", "ProjectCount", "StudyHours"
        ]
        df_empty = pd.DataFrame(columns=columns)
        df_empty.to_csv(user_file, index=False)
        
        df_durga = pd.read_csv("data/users/durga_gmail_com.csv")
        df_test = pd.read_csv(user_file)
        
        self.assertEqual(len(df_test), 0)
        self.assertEqual(len(df_durga), 1)
        print("Test Case 2 (Separate datasets for separate emails): PASSED")

if __name__ == "__main__":
    unittest.main()
