import streamlit as st
import pandas as pd
from utils.session_manager import initialize_session
from utils.kpi_utils import (
    calculate_total_problems,
    calculate_average_mock_score,
    calculate_total_applications,
    calculate_readiness_score
)
from utils.chart_utils import (
    create_problems_by_topic_chart,
    create_mock_score_trend_chart,
    create_application_trend_chart
)
from utils.ui_utils import render_logo, render_footer, render_empty_state, render_page_header

# Page configurations are managed globally by app.py
# st.set_page_config(
#     page_title="Placement Readiness Dashboard - HireReady",
#     page_icon="📊",
#     layout="wide"
# )






initialize_session()

# Render logo in the sidebar
render_logo(sidebar=True)

# Render standardized page header
render_page_header(
    "📊 Placement Readiness Dashboard", 
    "Monitor your unified career indicators and calculate your composite recruitment preparedness index."
)

# Verify session state data presence
if "historical_data" not in st.session_state or st.session_state["historical_data"] is None or st.session_state["historical_data"].empty:
    # Polished Empty State Panel
    render_empty_state(
        "No preparation data found.",
        [
            "Upload historical log sheets on the Data Import & Export Hub.",
            "Begin tracking your daily progress manually in the Progress Tracking Center."
        ]
    )
    
    st.markdown("---")
    
    # Render default/empty metric cards with neutral status placeholders
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Problems Solved", "0", help="Sum of all solved coding challenges.")
    col2.metric("Average Mock Score", "0.0%", help="Mean score across all mock sessions.")
    col3.metric("Total Applications", "0", help="Count of applications submitted.")
    col4.metric(
        "Placement Readiness Score", 
        "0.0 / 100", 
        help="Calculated using Problems Solved, Mock Scores, Applications, and Projects."
    )
    
    # Clean cached filters
    st.session_state["filtered_data"] = None
else:
    df_raw = st.session_state["historical_data"].copy()
    df_raw["Date"] = pd.to_datetime(df_raw["Date"])
    
    # ------------------ SIDEBAR FILTERS ------------------
    st.sidebar.header("🎯 Dashboard Filters")
    
    # 1. Topic Filter
    unique_topics = sorted(df_raw["Topic"].unique().tolist())
    selected_topics = st.sidebar.multiselect(
        "Select Topics",
        options=unique_topics,
        default=unique_topics,
        help="Filter dashboard metrics by specific coding topics."
    )
    
    # 2. Date Range Filter
    min_date_val = df_raw["Date"].min().date()  # type: ignore
    max_date_val = df_raw["Date"].max().date()  # type: ignore
    
    if min_date_val == max_date_val:
        selected_dates = st.sidebar.date_input("Date Range", value=min_date_val, help="Date range of preparation logs.")
        start_date = min_date_val
        end_date = max_date_val
    else:
        selected_dates = st.sidebar.date_input(
            "Date Range",
            value=(min_date_val, max_date_val),
            min_value=min_date_val,
            max_value=max_date_val,
            help="Select date range of preparation logs."
        )
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
        elif isinstance(selected_dates, tuple) and len(selected_dates) == 1:
            start_date = selected_dates[0]
            end_date = max_date_val
        else:
            start_date = min_date_val
            end_date = max_date_val
            
    # 3. Mock Score Range Filter
    min_mock = int(df_raw["MockScore"].min())
    max_mock = int(df_raw["MockScore"].max())
    slider_mock_val = (0, 100) if min_mock == max_mock else (min_mock, max_mock)
    selected_mock_range = st.sidebar.slider(
        "Mock Score Range (%)",
        min_value=0,
        max_value=100,
        value=slider_mock_val,
        help="Filter by mock interview scores."
    )
    
    # 4. Applications Range Filter
    min_apps = int(df_raw["Applications"].min())
    max_apps = int(df_raw["Applications"].max())
    slider_apps_val = (0, max_apps + 10) if min_apps == max_apps else (min_apps, max_apps)
    selected_apps_range = st.sidebar.slider(
        "Applications Count Range",
        min_value=0,
        max_value=max(10, max_apps + 5),
        value=slider_apps_val,
        help="Filter logs by applications count bounds."
    )
    
    # ------------------ APPLY FILTERS ------------------
    df_filtered = df_raw.copy()
    
    if selected_topics:
        df_filtered = df_filtered[df_filtered["Topic"].isin(selected_topics)]
    else:
        df_filtered = df_filtered.iloc[0:0]
        
    df_filtered = df_filtered[
        (df_filtered["Date"].dt.date >= start_date) & 
        (df_filtered["Date"].dt.date <= end_date)
    ]
    
    df_filtered = df_filtered[
        (df_filtered["MockScore"] >= selected_mock_range[0]) & 
        (df_filtered["MockScore"] <= selected_mock_range[1])
    ]
    
    df_filtered = df_filtered[
        (df_filtered["Applications"] >= selected_apps_range[0]) & 
        (df_filtered["Applications"] <= selected_apps_range[1])
    ]
    
    # Persist filtered dataset
    st.session_state["filtered_data"] = df_filtered
    
    # ------------------ RENDER KPIs & CHARTS ------------------
    if df_filtered.empty:
        # Polished Empty Filter State
        render_empty_state(
            "No data available for visualization.",
            [
                "Expand the Date Range in the sidebar filters.",
                "Select additional topics from the multiselect box.",
                "Widen the Mock Score Range slider bounds.",
                "Widen the Applications Range slider bounds."
            ]
        )
        
        st.markdown("---")
        
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric("Total Problems Solved", "0")
        kpi_col2.metric("Average Mock Score", "0.0%")
        kpi_col3.metric("Total Applications", "0")
        kpi_col4.metric(
            "Placement Readiness Score", 
            "0.0 / 100", 
            help="Calculated using Problems Solved, Mock Scores, Applications, and Projects."
        )
    else:
        st.markdown("### 📋 Filtered Dataset Summary")
        sum1, sum2, sum3 = st.columns(3)
        sum1.metric("Records Loaded", f"{len(df_filtered)} rows")
        sum2.metric("Topics Covered", f"{df_filtered['Topic'].nunique()}")
        f_min_date = df_filtered["Date"].min().strftime("%Y-%m-%d")
        f_max_date = df_filtered["Date"].max().strftime("%Y-%m-%d")
        
        # Render a custom HTML card to allow long dates to wrap without truncation
        sum3.markdown(
            f"""
            <div data-testid="metric-container" style="background: #131A26; border: 1px solid #1E293B; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); border-radius: 12px; padding: 18px 24px;">
                <label data-testid="stMetricLabel" style="font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8; display: block; margin-bottom: 8px;">Date Range</label>
                <div style="font-size: 1.6rem; font-weight: 700; background: linear-gradient(135deg, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; white-space: normal; word-break: break-word; line-height: 1.2;">
                    {f_min_date} to {f_max_date}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        total_problems = calculate_total_problems(df_filtered)
        avg_mock_score = calculate_average_mock_score(df_filtered)
        total_apps = calculate_total_applications(df_filtered)
        total_projects = int(df_filtered["ProjectCount"].sum()) if "ProjectCount" in df_filtered.columns else 0
        readiness_score = calculate_readiness_score(total_problems, avg_mock_score, total_apps, total_projects)
        
        st.markdown("### 🔑 Placement Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric(label="Total Problems Solved", value=str(total_problems))
        kpi_col2.metric(label="Average Mock Score", value=f"{avg_mock_score:.1f}%")
        kpi_col3.metric(label="Total Applications", value=str(total_apps))
        kpi_col4.metric(
            label="Placement Readiness Score", 
            value=f"{readiness_score} / 100",
            help="Calculated using Problems Solved, Mock Scores, Applications, and Projects."
        )
        
        st.markdown(
            '<p style="font-size: 0.85em; color: gray;">'
            '📊 <strong>Readiness Score Weights:</strong> 40% Problems Solved, 30% Mock Score, 20% Applications, 10% Projects'
            '</p>',
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        st.markdown("### 📈 Preparation Trends & Visualization")
        
        fig_problems = create_problems_by_topic_chart(df_filtered)
        if fig_problems:
            st.plotly_chart(fig_problems, width="stretch")
            
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_mock = create_mock_score_trend_chart(df_filtered)
            if fig_mock:
                st.plotly_chart(fig_mock, width="stretch")
        with chart_col2:
            fig_apps = create_application_trend_chart(df_filtered)
            if fig_apps:
                st.plotly_chart(fig_apps, width="stretch")



# Consistent Footer
render_footer()
