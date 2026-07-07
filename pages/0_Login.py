import streamlit as st
import os
import pandas as pd
from datetime import datetime
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
                # Create a new CSV with the standard schema
                os.makedirs("data/users", exist_ok=True)
                df_empty = pd.DataFrame(columns=columns)
                df_empty.to_csv(user_file, index=False)
                st.session_state["historical_data"] = df_empty
                st.toast(f"Created a new profile for {display_name}!")
            
            # Store login session state parameters
            st.session_state["user_name"] = display_name
            st.session_state["user_email"] = cleaned_email
            st.session_state["user_file"] = user_file
            st.session_state["is_logged_in"] = True
            st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Programmatic rerun to trigger navigation routing to Dashboard
            st.rerun()
