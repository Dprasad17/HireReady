import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
from utils.session_manager import initialize_session
from utils.job_api import fetch_jobs
from utils.map_utils import CITY_COORDINATES, DEFAULT_CENTER, create_job_map
from utils.ui_utils import render_logo, render_footer, render_empty_state, render_page_header

# Page configurations are managed globally by app.py
# st.set_page_config(
#     page_title="Live Opportunities Explorer - HireReady",
#     page_icon="💼",
#     layout="wide"
# )

initialize_session()

# Render logo in the sidebar
render_logo(sidebar=True)

# Render standardized page header
render_page_header(
    "💼 Live Opportunities Explorer",
    "Browse current opportunities, filter by location type, and inspect postings on the interactive map."
)

# Initialize page search session states
if "jobs_search_results" not in st.session_state:
    st.session_state["jobs_search_results"] = []
if "jobs_map_center" not in st.session_state:
    st.session_state["jobs_map_center"] = DEFAULT_CENTER
if "jobs_search_executed" not in st.session_state:
    st.session_state["jobs_search_executed"] = False

# Layout Grid: Inputs on Left, Map & Table on Right
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 🔍 Filter Opportunities")
    
    role_input = st.text_input(
        "Role Keyword", 
        placeholder="e.g. Developer, Data, Designer",
        help="Filter jobs by title terms (e.g. Software, Data)."
    )
    
    location_list = list(CITY_COORDINATES.keys())
    location_input = st.selectbox(
        "Location City", 
        options=location_list,
        help="Select location to explore opportunities."
    )
    
    job_type_input = st.selectbox(
        "Job Type", 
        options=["Full-Time", "Internship"],
        help="Filter openings by work classification."
    )
    
    search_triggered = st.button("Search Openings", width="stretch")
    
    if search_triggered:
        # Add loading spinner
        with st.spinner("Searching live opportunities..."):
            try:
                jobs = fetch_jobs(role_input, location_input, job_type_input)
                
                st.session_state["jobs_search_results"] = jobs
                st.session_state["jobs_map_center"] = CITY_COORDINATES[location_input]
                st.session_state["jobs_search_executed"] = True
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ API Failure: {str(e)}")
                st.session_state["jobs_search_results"] = []
                st.session_state["jobs_search_executed"] = True

with col_right:
    results = st.session_state["jobs_search_results"]
    center = st.session_state["jobs_map_center"]
    searched = st.session_state["jobs_search_executed"]
    
    if searched:
        if not results:
            # Polished empty search state
            render_empty_state(
                "No opportunities matched the selected criteria.",
                [
                    "Try a broader keyword",
                    "Leave the role field empty",
                    "Switch between Internship and Full-Time"
                ]
            )

            
            st.markdown("---")
            
            # Empty state KPIs
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            kpi_col1.metric("Total Openings", "0")
            kpi_col2.metric("Unique Companies", "0")
            kpi_col3.metric("Unique Locations", "0")
        else:
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            kpi_col1.metric("Total Openings", str(len(results)))
            
            unique_companies = len(set(j["company"] for j in results))
            kpi_col2.metric("Unique Companies", str(unique_companies))
            
            unique_locations = len(set(j["location"] for j in results))
            kpi_col3.metric("Unique Locations", str(unique_locations))
            
        st.markdown("### 🗺️ Location Plot Mapping")
        
        try:
            job_map = create_job_map(results, center)
            st_folium(job_map, height=400, use_container_width=True, key="job_explorer_map")
        except Exception as e:
            st.error(f"Failed to load map canvas: {str(e)}")
            
        if results:
            st.markdown("### 📋 Postings List")
            df_jobs = pd.DataFrame(results)
            
            df_display = df_jobs[["company", "role", "location", "job_type", "apply_url"]].copy()
            df_display.columns = ["Company", "Role", "Location", "Job Type", "Apply URL"]
            
            st.dataframe(
                df_display,
                column_config={
                    "Apply URL": st.column_config.LinkColumn("Apply Link", display_text="Open Posting ↗️")
                },
                width="stretch",
                hide_index=True
            )
            
    else:
        st.info("💡 **Welcome**: Enter your search query on the left to explore live recruitment data.")
        st.markdown("### 🗺️ Default Interactive Map (India)")
        
        try:
            default_map = create_job_map([], DEFAULT_CENTER)
            st_folium(default_map, height=450, use_container_width=True, key="default_explorer_map")
        except Exception as e:
            st.error(f"Failed to load default map canvas: {str(e)}")

# Consistent Footer
render_footer()
