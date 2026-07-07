"""
Data utility functions for importing, validating, and cleaning CSV and Excel datasets.
"""
import pandas as pd
import numpy as np

# Locked schema for HireReady Phase 2
REQUIRED_COLUMNS = [
    "Date",
    "Topic",
    "ProblemsSolved",
    "MockScore",
    "Applications",
    "ProjectCount",
    "StudyHours"
]

def load_csv(file_obj) -> pd.DataFrame:
    """
    Loads historical student data from a CSV file object.

    Args:
        file_obj: File-like object uploaded via Streamlit.

    Returns:
        pd.DataFrame: Loaded dataset frame.
    """
    return pd.read_csv(file_obj)

def load_excel(file_obj) -> pd.DataFrame:
    """
    Loads historical student data from an Excel (.xlsx) file object.

    Args:
        file_obj: File-like object uploaded via Streamlit.

    Returns:
        pd.DataFrame: Loaded dataset frame.
    """
    return pd.read_excel(file_obj)

def validate_dataset(df: pd.DataFrame) -> tuple[bool, str, list]:
    """
    Validates that all required columns are present and data is not empty.
    Identifies if there are extra columns.

    Args:
        df (pd.DataFrame): Ingested dataframe.

    Returns:
        tuple: (is_valid: bool, error_message: str, extra_columns: list)
    """
    if df is None or df.empty:
        return False, "Uploaded dataset is empty.", []
    
    # Check for missing required columns (case sensitive)
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}", []
        
    # Find extra columns
    extra_cols = [col for col in df.columns if col not in REQUIRED_COLUMNS]
    
    return True, "", extra_cols

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by:
    1. Keeping only required columns (dropping extra columns).
    2. Converting Date column using pandas datetime.
    3. Parsing numeric types, setting invalid values to NaN, and filling missing values.
    4. Handling missing topics.
    5. Dropping duplicates.

    Args:
        df (pd.DataFrame): Validated dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    # Keep only the required columns
    cleaned_df = df[REQUIRED_COLUMNS].copy()
    
    # 1. Clean Dates (coerce errors, drop rows with invalid dates if needed, or fill them)
    cleaned_df["Date"] = pd.to_datetime(cleaned_df["Date"], errors="coerce")
    
    # Drop rows where Date is NaT
    cleaned_df = cleaned_df.dropna(subset=["Date"])
    
    # 2. Clean Topic (string)
    cleaned_df["Topic"] = cleaned_df["Topic"].astype(str).str.strip()
    cleaned_df["Topic"] = cleaned_df["Topic"].replace(["nan", "None", ""], "General")
    
    # 3. Clean numeric columns
    numeric_cols = ["ProblemsSolved", "MockScore", "Applications", "ProjectCount", "StudyHours"]
    for col in numeric_cols:
        cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")
        # Fill missing numeric values with 0
        cleaned_df[col] = cleaned_df[col].fillna(0)
        
    # Convert integer counts explicitly to integers
    int_cols = ["ProblemsSolved", "Applications", "ProjectCount"]
    for col in int_cols:
        cleaned_df[col] = cleaned_df[col].astype(int)
        
    # Convert scores and hours to floats
    float_cols = ["MockScore", "StudyHours"]
    for col in float_cols:
        cleaned_df[col] = cleaned_df[col].astype(float)
        
    # 4. Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()
    
    # Sort by Date ascending
    cleaned_df = cleaned_df.sort_values(by="Date").reset_index(drop=True)
    
    return cleaned_df
