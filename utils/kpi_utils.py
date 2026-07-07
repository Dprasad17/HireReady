"""
KPI utility functions for computing student readiness analytics.
"""
import pandas as pd

def calculate_total_problems(df: pd.DataFrame) -> int:
    """
    Computes total problems solved from the preparation dataset.
    Safely handles empty datasets by returning 0.

    Args:
        df (pd.DataFrame): Candidate logs.

    Returns:
        int: Sum of problems solved.
    """
    if df is None or df.empty or "ProblemsSolved" not in df.columns:
        return 0
    return int(df["ProblemsSolved"].sum())

def calculate_average_mock_score(df: pd.DataFrame) -> float:
    """
    Computes the mean mock interview score from the preparation dataset.
    Safely handles empty datasets by returning 0.0.

    Args:
        df (pd.DataFrame): Candidate logs.

    Returns:
        float: Average mock interview score.
    """
    if df is None or df.empty or "MockScore" not in df.columns:
        return 0.0
    # Calculate average only for entries with actual data or average of all
    return df["MockScore"].mean()

def calculate_total_applications(df: pd.DataFrame) -> int:
    """
    Computes total applications submitted from the preparation dataset.
    Safely handles empty datasets by returning 0.

    Args:
        df (pd.DataFrame): Candidate logs.

    Returns:
        int: Sum of applications submitted.
    """
    if df is None or df.empty or "Applications" not in df.columns:
        return 0
    return int(df["Applications"].sum())

def calculate_readiness_score(total_problems: int, avg_mock_score: float, total_applications: int, total_projects: int) -> float:
    """
    Computes a placement readiness index score out of 100 based on weighted metrics:
    - Problems Solved (40%, Target = 200)
    - Average Mock Score (30%, Target = 100)
    - Total Applications (20%, Target = 20)
    - Total Projects Completed (10%, Target = 4)

    Args:
        total_problems (int): Total DSA problems solved.
        avg_mock_score (float): Average mock interview score.
        total_applications (int): Total applications submitted.
        total_projects (int): Total projects completed.

    Returns:
        float: Weighted placement readiness score between 0.0 and 100.0.
    """
    # Safeguard inputs
    total_problems = max(0, total_problems)
    avg_mock_score = max(0.0, avg_mock_score)
    total_applications = max(0, total_applications)
    total_projects = max(0, total_projects)

    # 1. Problems Solved (40% Weight, Target 200)
    problems_contrib = min((total_problems / 200.0) * 40.0, 40.0)

    # 2. Mock Score (30% Weight, Target 100)
    mock_contrib = min((avg_mock_score / 100.0) * 30.0, 30.0)

    # 3. Applications (20% Weight, Target 20)
    apps_contrib = min((total_applications / 20.0) * 20.0, 20.0)

    # 4. Projects (10% Weight, Target 4)
    projects_contrib = min((total_projects / 4.0) * 10.0, 10.0)

    # Composite score calculation
    readiness_score = problems_contrib + mock_contrib + apps_contrib + projects_contrib
    return round(readiness_score, 2)
