import streamlit as st
import os
import pandas as pd
from datetime import datetime
from utils.session_manager import initialize_session
from utils.data_utils import load_csv, load_excel, validate_dataset, clean_dataset
from utils.export_utils import generate_dataset_export, generate_readiness_report
from utils.ui_utils import render_logo, render_footer, render_empty_state, render_page_header

# Page configurations are managed globally by app.py
# st.set_page_config(
#     page_title="Data Import & Export Hub - HireReady",
#     page_icon="💾",
#     layout="wide"
# )

initialize_session()

# Render logo in the sidebar
render_logo(sidebar=True)

# Render standardized page header
render_page_header(
    "📁 Data Import & Export Hub", 
    "Import your historical preparation logs or export readiness reports and datasets."
)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📥 Upload Your Historical Preparation Data")
    st.write("Provide your placement preparation history to initialize your readiness scores.")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel (.xlsx) file", 
        type=["csv", "xlsx"],
        help="Upload CSV or Excel files following the required schema."
    )
    
    df_raw = None
    file_source_name = None

    # Handle manual file upload
    if uploaded_file is not None:
        file_source_name = uploaded_file.name
        try:
            if file_source_name.endswith(".csv"):
                df_raw = load_csv(uploaded_file)
            elif file_source_name.endswith(".xlsx"):
                df_raw = load_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload a .csv or .xlsx file.")
        except Exception as e:
            st.error(f"Failed to read file: The file might be corrupted or in an invalid format. Error: {str(e)}")

    # Process and validate data if loaded
    if df_raw is not None:
        st.markdown("---")
        st.markdown(f"#### ⚙️ Processing: `{file_source_name}`")
        
        # 1. Validate dataset (wrapped in spinner as requested)
        with st.spinner("Validating uploaded dataset..."):
            is_valid, error_msg, extra_cols = validate_dataset(df_raw)
        
        if not is_valid:
            st.error(f"❌ Validation Failed: {error_msg}")
        else:
            # Show warning if there are extra columns
            if extra_cols:
                st.warning(f"⚠️ Warning: Extra columns detected and will be ignored: {', '.join(extra_cols)}")
            else:
                st.success("✅ Schema matches the locked HireReady specifications.")
            
            # 2. Clean dataset
            try:
                with st.spinner("Cleaning and structuring dataset..."):
                    cleaned_df = clean_dataset(df_raw)
                
                if cleaned_df.empty:
                    st.error("❌ Cleaning Failed: No valid records left after removing invalid dates.")
                else:
                    # 3. Store in session state
                    st.session_state["historical_data"] = cleaned_df
                    
                    # Auto-save to user file
                    user_file = st.session_state.get("user_file")
                    if user_file:
                        cleaned_df.to_csv(user_file, index=False)
                        st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                    st.success("💾 Dataset stored successfully in Session State.")
                    
                    # 4. Display Summary Metrics
                    st.markdown("#### 📊 Dataset Summary")
                    sum_col1, sum_col2, sum_col3 = st.columns(3)
                    
                    # Records Loaded
                    records_count = len(cleaned_df)
                    sum_col1.metric("Records Loaded", f"{records_count} rows")
                    
                    # Unique Topics
                    unique_topics = cleaned_df["Topic"].nunique()
                    sum_col2.metric("Topics Found", str(unique_topics))
                    
                    # Date Range
                    min_date = str(cleaned_df["Date"].min())[:10]
                    max_date = str(cleaned_df["Date"].max())[:10]
                    sum_col3.metric("Date Range", f"{min_date} to {max_date}")
                    
                    # 5. Display Preview
                    st.markdown("#### 🔍 Cleaned Data Preview")
                    preview_df = cleaned_df.copy()
                    preview_df["Date"] = [str(d)[:10] for d in preview_df["Date"]]
                    st.dataframe(preview_df, width="stretch")
                    
            except Exception as e:
                st.error(f"❌ Error cleaning dataset: {str(e)}")

with col2:
    st.markdown("### 📤 Export Preparation Data")
    
    # Check if data exists in memory
    if "historical_data" in st.session_state and st.session_state["historical_data"] is not None and not st.session_state["historical_data"].empty:
        # Determine active dataset target (Filtered vs Full) using standardized selection logic
        filtered_data = st.session_state.get("filtered_data")

        if filtered_data is not None and not filtered_data.empty:
            export_df = filtered_data
            dataset_scope = "Filtered Dataset"
        else:
            export_df = st.session_state["historical_data"]
            dataset_scope = "Full Dataset"
            
        st.info(f"💡 **Export Source**: Current {dataset_scope} ({len(export_df)} rows active).")
            
        # 1. Dataset Export (CSV)
        csv_bytes = generate_dataset_export(export_df)
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_bytes,
            file_name="hire_ready_dataset.csv",
            mime="text/csv",
            width="stretch"
        )
        
        # 2. Report Export (TXT)
        with st.spinner("Generating placement report..."):
            report_text = generate_readiness_report(export_df, dataset_scope)
            
        st.download_button(
            label="📄 Download Placement Report (TXT)",
            data=report_text,
            file_name="placement_readiness_report.txt",
            mime="text/plain",
            width="stretch"
        )
        
    else:
        # Polished empty state
        render_empty_state(
            "No dataset available.",
            [
                "Upload a historical dataset on the left panel to initialize reports.",
                "Or manually record preparation activity in the Progress Tracking Center."
            ]
        )
        st.button("📥 Download Dataset (Disabled)", disabled=True, width="stretch")
        st.button("📄 Download Placement Report (Disabled)", disabled=True, width="stretch")
    
    st.markdown("---")
    st.markdown("### 💾 Current Session State Status")
    if "historical_data" in st.session_state and st.session_state["historical_data"] is not None:
        st.success(f"✔️ Active data loaded in session state ({len(st.session_state['historical_data'])} rows)")
        if st.button("🗑️ Reset Dataset"):
            columns = [
                "Date", "Topic", "ProblemsSolved", "MockScore", 
                "Applications", "ProjectCount", "StudyHours"
            ]
            df_empty = pd.DataFrame(columns=columns)
            st.session_state["historical_data"] = df_empty
            
            # Overwrite user file on disk
            user_file = st.session_state.get("user_file")
            if user_file and os.path.exists(user_file):
                df_empty.to_csv(user_file, index=False)
                
            st.session_state["last_saved"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if "filtered_data" in st.session_state:
                del st.session_state["filtered_data"]
            st.rerun()
    else:
        st.warning("⚠️ No historical placement data loaded in memory yet.")

# Consistent Footer
render_footer()
