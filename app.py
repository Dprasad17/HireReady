import streamlit as st
import os
import pandas as pd
from datetime import datetime
from utils.session_manager import initialize_session

# Global Page Configurations (Must be called exactly once before any pages execute)
st.set_page_config(
    page_title="HireReady - Placement Readiness Intelligence Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
initialize_session()

# Initialize Login State if not present
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

# Navigation Page Configurations
if not st.session_state["is_logged_in"]:
    # Block access to subpages and show only Login page
    login_page = st.Page("pages/0_Login.py", title="Login", icon="🔑", default=True)
    pg = st.navigation([login_page], position="hidden")
else:
    # Authenticated navigation
    dashboard_page = st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊", default=True)
    job_explorer_page = st.Page("pages/2_Job_Explorer.py", title="Job Explorer", icon="💼")
    progress_tracker_page = st.Page("pages/3_Progress_Tracker.py", title="Progress Tracker", icon="📝")
    import_export_page = st.Page("pages/4_Import_Export.py", title="Import Export", icon="📁")
    
    pg = st.navigation([
        dashboard_page,
        job_explorer_page,
        progress_tracker_page,
        import_export_page
    ])

    # Render Logged In User Profile Card in Sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 Logged In User")
        st.write(f"**Name:** {st.session_state.get('user_name', 'Unknown')}")
        st.write(f"**Email:** {st.session_state.get('user_email', 'Unknown')}")
        
        # Calculate active records count safely
        count = 0
        if "historical_data" in st.session_state and st.session_state["historical_data"] is not None:
            count = len(st.session_state["historical_data"])
        st.write(f"**Records Count:** {count}")
        st.write(f"**Last Saved:** {st.session_state.get('last_saved', 'N/A')}")
        
        st.markdown("---")
        
        # Logout Trigger (Does NOT delete files)
        if st.button("Logout", key="logout_btn", width="stretch"):
            st.session_state["user_name"] = None
            st.session_state["user_email"] = None
            st.session_state["user_file"] = None
            st.session_state["historical_data"] = None
            st.session_state["is_logged_in"] = False
            st.session_state["last_saved"] = None
            st.rerun()
            
        # Reset Dataset Trigger (Clears table and overwrites active user file to empty)
        if st.button("⚠️ Reset Dataset", key="reset_dataset_btn", width="stretch"):
            columns = [
                "Date", "Topic", "ProblemsSolved", "MockScore", 
                "Applications", "ProjectCount", "StudyHours"
            ]
            df_empty = pd.DataFrame(columns=columns)
            st.session_state["historical_data"] = df_empty
            
            # Overwrite the active user file immediately
            user_file = st.session_state.get("user_file")
            if user_file and os.path.exists(user_file):
                df_empty.to_csv(user_file, index=False)
                
            st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.toast("Active dataset reset successfully!")
            st.rerun()

# Run navigation script routing
pg.run()
