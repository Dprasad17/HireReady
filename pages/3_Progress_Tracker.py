import streamlit as st
import pandas as pd
from datetime import datetime
from utils.session_manager import initialize_session
from utils.data_utils import REQUIRED_COLUMNS
from utils.ui_utils import render_logo, render_footer, render_empty_state, render_page_header

# Page configurations are managed globally by app.py
# st.set_page_config(
#     page_title="Progress Tracking Center - HireReady",
#     page_icon="📝",
#     layout="wide"
# )

initialize_session()

# Render logo in the sidebar
render_logo(sidebar=True)

# Render standardized page header
render_page_header(
    "📝 Progress Tracking Center", 
    "Track your daily preparation efforts. All entries are saved directly in your session storage."
)

col_form, col_history = st.columns([2, 3])

with col_form:
    st.markdown("### ➕ Log Daily Progress")
    
    # Define form layout with standard tooltip
    with st.form("progress_form", clear_on_submit=True):
        entry_date = st.date_input(
            "Date", 
            value=datetime.today(),
            help="Select the date for logging your preparation activities."
        )
        topic = st.text_input(
            "Topic", 
            placeholder="e.g. Dynamic Programming, System Design",
            help="Log daily placement preparation activities."
        )
        
        form_col1, form_col2 = st.columns(2)
        problems_solved = form_col1.number_input(
            "DSA Problems Solved", 
            min_value=0, 
            value=0, 
            step=1,
            help="Count of DSA coding challenges solved today."
        )
        mock_score = form_col2.number_input(
            "Mock Interview Score (%)", 
            min_value=0, 
            max_value=100, 
            value=0, 
            step=1,
            help="Score received in mock interview session."
        )
        
        form_col3, form_col4, form_col5 = st.columns(3)
        applications = form_col3.number_input("Applications Sent", min_value=0, value=0, step=1)
        project_count = form_col4.number_input("Projects Completed", min_value=0, value=0, step=1)
        study_hours = form_col5.number_input("Study Hours", min_value=0.0, value=0.0, step=0.5)
        
        submit_button = st.form_submit_button("Save Progress Entry")
        
        if submit_button:
            validation_errors = []
            
            cleaned_topic = topic.strip()
            if not cleaned_topic:
                validation_errors.append("Topic cannot be empty.")
            
            if problems_solved < 0:
                validation_errors.append("Problems Solved cannot be negative.")
            if mock_score < 0 or mock_score > 100:
                validation_errors.append("Mock Score must be between 0 and 100.")
            if applications < 0:
                validation_errors.append("Applications cannot be negative.")
            if project_count < 0:
                validation_errors.append("Project Count cannot be negative.")
            if study_hours < 0:
                validation_errors.append("Study Hours cannot be negative.")
                
            if entry_date is None:
                validation_errors.append("Please enter a valid date.")
                
            if validation_errors:
                for error in validation_errors:
                    st.error(f"❌ Input Error: {error}")
            else:
                if "historical_data" not in st.session_state or st.session_state["historical_data"] is None:
                    st.session_state["historical_data"] = pd.DataFrame(columns=REQUIRED_COLUMNS)
                
                df = st.session_state["historical_data"]
                
                new_row = pd.DataFrame([{
                    "Date": pd.to_datetime(entry_date),
                    "Topic": cleaned_topic,
                    "ProblemsSolved": problems_solved,
                    "MockScore": mock_score,
                    "Applications": applications,
                    "ProjectCount": project_count,
                    "StudyHours": study_hours
                }])
                
                df = pd.concat([df, new_row], ignore_index=True)
                df = df.sort_values(by="Date").reset_index(drop=True)
                
                st.session_state["historical_data"] = df
                
                # Auto-save to user file
                user_file = st.session_state.get("user_file")
                if user_file:
                    df.to_csv(user_file, index=False)
                    st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                st.success("✅ Progress entry logged successfully!")
                st.rerun()

with col_history:
    st.markdown("### 📋 Preparation Logs History")
    
    if "historical_data" in st.session_state and st.session_state["historical_data"] is not None and not st.session_state["historical_data"].empty:
        df = st.session_state["historical_data"].copy()
        df["Date"] = pd.to_datetime(df["Date"])
        
        sum1, sum2, sum3 = st.columns(3)
        sum1.metric("Total Records", f"{len(df)}")
        sum2.metric("Topics Covered", f"{df['Topic'].nunique()}")
        latest_date_val = df["Date"].max()  # type: ignore
        latest_date_str = str(latest_date_val)[:10] if pd.notnull(latest_date_val) else "N/A"
        sum3.metric("Latest Entry Date", latest_date_str)
        
        delete_btn = st.button("🗑️ Delete Last Entry")
        if delete_btn:
            df = df.iloc[:-1].reset_index(drop=True)
            st.session_state["historical_data"] = df
            
            # Auto-save to user file
            user_file = st.session_state.get("user_file")
            if user_file:
                df.to_csv(user_file, index=False)
                st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            st.warning("⚠️ Most recent log entry removed.")
            st.rerun()
            
        st.markdown("---")
        
        preview_df = df.copy()
        preview_df["Date"] = preview_df["Date"].dt.strftime("%Y-%m-%d")
        st.dataframe(preview_df, width="stretch")

    else:
        # Polished empty state
        render_empty_state(
            "No entries recorded yet.",
            [
                "Use the Log Daily Progress form on the left to add a record.",
                "Or navigate to the Import page to upload historical spreadsheet files."
            ]
        )

# Consistent Footer
render_footer()
