import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
from utils.session_manager import load_profiles, save_profile

# Main title header
st.title("🔑 HireReady User Login")
st.subheader("Login or register using your email address to persist your preparation dataset.")

st.markdown("---")

col_form, _ = st.columns([2, 1])

with col_form:
    name_input = st.text_input("Full Name")
    email_input = st.text_input("Email Address")
    
    continue_btn = st.button("Continue", width="stretch")
    
    if continue_btn:
        cleaned_name = name_input.strip()
        cleaned_email = email_input.strip().lower()
        
        # Validation checks
        if not cleaned_name:
            st.error("❌ Name cannot be empty.")
        elif not cleaned_email or "@" not in cleaned_email:
            st.error("❌ Please enter a valid email address containing '@'.")
        else:
            # Safe filename mapping
            safe_email = cleaned_email.replace("@", "_").replace(".", "_")
            user_file = f"data/users/{safe_email}.csv"
            
            # Save metadata mapping in profiles.json
            profiles = load_profiles()
            user_meta = profiles.get(cleaned_email)
            
            # Resolve name (use existing name if returning user, else the entered name)
            display_name = user_meta["name"] if user_meta else cleaned_name
            save_profile(cleaned_email, display_name)
            
            # Check CSV file existence
            columns = [
                "Date", "Topic", "ProblemsSolved", "MockScore", 
                "Applications", "ProjectCount", "StudyHours"
            ]
            
            if os.path.exists(user_file):
                try:
                    df = pd.read_csv(user_file)
                    df["Date"] = pd.to_datetime(df["Date"])
                    st.session_state["historical_data"] = df
                    st.toast(f"Welcome back, {display_name}! Loaded your saved records.")
                except Exception as e:
                    st.error(f"Error loading saved dataset: {str(e)}")
                    # Initial empty dataset on load error
                    st.session_state["historical_data"] = pd.DataFrame(columns=columns)
            else:
                # Pre-populate new users with realistic mock placement data so they see a working dashboard instantly
                os.makedirs("data/users", exist_ok=True)
                
                # Generate dates relative to today
                today = datetime.today()
                
                mock_records = [
                    {
                        "Date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
                        "Topic": "Arrays & Hashing",
                        "ProblemsSolved": 12,
                        "MockScore": 70.0,
                        "Applications": 2,
                        "ProjectCount": 0,
                        "StudyHours": 4.5
                    },
                    {
                        "Date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
                        "Topic": "Linked Lists",
                        "ProblemsSolved": 8,
                        "MockScore": 0.0,
                        "Applications": 3,
                        "ProjectCount": 1,
                        "StudyHours": 3.5
                    },
                    {
                        "Date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
                        "Topic": "SQL Databases",
                        "ProblemsSolved": 15,
                        "MockScore": 78.0,
                        "Applications": 4,
                        "ProjectCount": 0,
                        "StudyHours": 5.0
                    },
                    {
                        "Date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                        "Topic": "Dynamic Programming",
                        "ProblemsSolved": 6,
                        "MockScore": 85.0,
                        "Applications": 2,
                        "ProjectCount": 1,
                        "StudyHours": 6.0
                    },
                    {
                        "Date": today.strftime("%Y-%m-%d"),
                        "Topic": "System Design",
                        "ProblemsSolved": 5,
                        "MockScore": 90.0,
                        "Applications": 5,
                        "ProjectCount": 1,
                        "StudyHours": 4.5
                    }
                ]
                
                df_mock = pd.DataFrame(mock_records)
                df_mock["Date"] = pd.to_datetime(df_mock["Date"])
                df_mock.to_csv(user_file, index=False)
                st.session_state["historical_data"] = df_mock
                st.toast(f"Created a profile for {display_name} with sample placement data!")
            
            # Store login session state parameters
            st.session_state["user_name"] = display_name
            st.session_state["user_email"] = cleaned_email
            st.session_state["user_file"] = user_file
            st.session_state["is_logged_in"] = True
            st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Programmatic rerun to trigger navigation routing to Dashboard
            st.rerun()
