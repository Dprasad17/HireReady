"""
Session state manager for centralizing application state and student tracker metrics.
"""
import streamlit as st
import os
import json

def initialize_session():
    """
    Initialize application session state parameters.
    Creates default placeholders for student progress inputs and profile details if not present.
    """
    if "student_name" not in st.session_state:
        st.session_state["student_name"] = "Ready Candidate"
    if "dsa_solved" not in st.session_state:
        st.session_state["dsa_solved"] = 0
    if "mocks_completed" not in st.session_state:
        st.session_state["mocks_completed"] = 0
    if "resume_score" not in st.session_state:
        st.session_state["resume_score"] = 0.0

def load_profiles() -> dict:
    """
    Loads user profile metadata from data/users/profiles.json.
    """
    profiles_path = "data/users/profiles.json"
    if not os.path.exists("data/users"):
        os.makedirs("data/users", exist_ok=True)
    if os.path.exists(profiles_path):
        try:
            with open(profiles_path, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_profile(email: str, name: str):
    """
    Saves or updates a user profile name in data/users/profiles.json.
    """
    profiles_path = "data/users/profiles.json"
    if not os.path.exists("data/users"):
        os.makedirs("data/users", exist_ok=True)
    profiles = load_profiles()
    profiles[email.strip().lower()] = {
        "name": name.strip()
    }
    try:
        with open(profiles_path, "w") as f:
            json.dump(profiles, f, indent=4)
    except Exception as e:
        st.error(f"Error saving profile metadata: {str(e)}")
