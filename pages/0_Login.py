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
            
            should_populate_mock = False
            if os.path.exists(user_file):
                try:
                    df = pd.read_csv(user_file)
                    if df.empty:
                        should_populate_mock = True
                    else:
                        df["Date"] = pd.to_datetime(df["Date"])
                        st.session_state["historical_data"] = df
                        st.toast(f"Welcome back, {display_name}! Loaded your saved records.")
                except Exception as e:
                    should_populate_mock = True
            else:
                should_populate_mock = True

            if should_populate_mock:
                # Pre-populate new users with realistic mock placement data so they see a working dashboard instantly
                os.makedirs("data/users", exist_ok=True)
                
                # Generate dates relative to today (covering last 14 days, with some gaps, showing improvement over time)
                today = datetime.today()
                
                mock_records = [
                    {
                        "Date": (today - timedelta(days=14)).strftime("%Y-%m-%d"),
                        "Topic": "Arrays & Hashing",
                        "ProblemsSolved": 8,
                        "MockScore": 60.0,
                        "Applications": 1,
                        "ProjectCount": 0,
                        "StudyHours": 3.0
                    },
                    {
                        "Date": (today - timedelta(days=12)).strftime("%Y-%m-%d"),
                        "Topic": "Two Pointers",
                        "ProblemsSolved": 10,
                        "MockScore": 65.0,
                        "Applications": 2,
                        "ProjectCount": 0,
                        "StudyHours": 4.0
                    },
                    {
                        "Date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
                        "Topic": "Sliding Window",
                        "ProblemsSolved": 6,
                        "MockScore": 62.0,
                        "Applications": 1,
                        "ProjectCount": 1,
                        "StudyHours": 3.5
                    },
                    {
                        "Date": (today - timedelta(days=8)).strftime("%Y-%m-%d"),
                        "Topic": "Stacks & Queues",
                        "ProblemsSolved": 12,
                        "MockScore": 70.0,
                        "Applications": 3,
                        "ProjectCount": 0,
                        "StudyHours": 5.0
                    },
                    {
                        "Date": (today - timedelta(days=6)).strftime("%Y-%m-%d"),
                        "Topic": "Binary Search",
                        "ProblemsSolved": 14,
                        "MockScore": 75.0,
                        "Applications": 4,
                        "ProjectCount": 1,
                        "StudyHours": 5.5
                    },
                    {
                        "Date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
                        "Topic": "Trees & Graphs",
                        "ProblemsSolved": 18,
                        "MockScore": 82.0,
                        "Applications": 5,
                        "ProjectCount": 0,
                        "StudyHours": 6.5
                    },
                    {
                        "Date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
                        "Topic": "Dynamic Programming",
                        "ProblemsSolved": 10,
                        "MockScore": 80.0,
                        "Applications": 6,
                        "ProjectCount": 1,
                        "StudyHours": 7.0
                    },
                    {
                        "Date": today.strftime("%Y-%m-%d"),
                        "Topic": "System Design",
                        "ProblemsSolved": 5,
                        "MockScore": 88.0,
                        "Applications": 4,
                        "ProjectCount": 1,
                        "StudyHours": 6.0
                    }
                ]
                
                df_mock = pd.DataFrame(mock_records)
                df_mock["Date"] = pd.to_datetime(df_mock["Date"])
                df_mock.to_csv(user_file, index=False)
                st.session_state["historical_data"] = df_mock
                st.toast(f"Created profile for {display_name} with sample placement data!")
            
            # Store login session state parameters
            st.session_state["user_name"] = display_name
            st.session_state["user_email"] = cleaned_email
            st.session_state["user_file"] = user_file
            st.session_state["is_logged_in"] = True
            st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Programmatic rerun to trigger navigation routing to Dashboard
            st.rerun()
