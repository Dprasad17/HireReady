"""
Data export utility functions for compiling datasets and generating placement readiness text reports.
"""
from datetime import datetime
import pandas as pd
from utils.kpi_utils import (
    calculate_total_problems,
    calculate_average_mock_score,
    calculate_total_applications,
    calculate_readiness_score
)

def generate_dataset_export(df: pd.DataFrame) -> bytes:
    """
    Converts the provided candidate dataframe to standard CSV bytes.

    Args:
        df (pd.DataFrame): Candidate logs.

    Returns:
        bytes: Encoded CSV byte data.
    """
    if df is None:
        return b""
    return df.to_csv(index=False).encode("utf-8")

def generate_readiness_report(df: pd.DataFrame, scope: str) -> str:
    """
    Generates a plaintext placement readiness report compiling KPI indicators,
    caching details, and custom rule-based recommendations.

    Args:
        df (pd.DataFrame): Student logs.
        scope (str): Indicator of dataset scope ("Filtered Dataset" or "Full Dataset").

    Returns:
        str: Formatted plaintext report structure.
    """
    if df is None:
        return "No data available."

    # Compute KPI totals reusing calculations
    total_problems = calculate_total_problems(df)
    avg_mock_score = calculate_average_mock_score(df)
    total_apps = calculate_total_applications(df)
    total_projects = int(df["ProjectCount"].sum()) if "ProjectCount" in df.columns else 0
    readiness_score = calculate_readiness_score(total_problems, avg_mock_score, total_apps, total_projects)

    # Compile Rule-based Recommendations
    recommendations = []
    
    if total_problems < 200:
        recommendations.append("Increase problem-solving practice (Target: 200 solved).")
    
    if total_apps < 20:
        recommendations.append("Submit more applications (Target: 20 applications).")
        
    if total_projects < 4:
        recommendations.append("Build additional projects (Target: 4 completed).")
        
    if avg_mock_score >= 80.0:
        recommendations.append("Maintain mock interview performance.")
    else:
        recommendations.append("Improve mock interview performance (Aim for 80%+).")

    # Formulate plain text report template
    report = []
    report.append("==================================================")
    report.append("       HireReady Placement Readiness Report       ")
    report.append("==================================================")
    report.append(f"Generated Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Dataset Scope  : {scope}")
    report.append("--------------------------------------------------")
    report.append("📊 PREPARATION STATS SUMMARY")
    report.append(f"  - Total Problems Solved      : {total_problems}")
    report.append(f"  - Average Mock Score         : {avg_mock_score:.1f}%")
    report.append(f"  - Applications Submitted     : {total_apps}")
    report.append(f"  - Projects Completed         : {total_projects}")
    report.append(f"  - Placement Readiness Score  : {readiness_score} / 100")
    report.append("--------------------------------------------------")
    
    report.append("💡 CAREER PREPARATION RECOMMENDATIONS")
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            report.append(f"  {idx}. {rec}")
    else:
        report.append("  - Keep up the great work! All preparation metrics look solid.")
    report.append("==================================================")
    
    return "\n".join(report)
