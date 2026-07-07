"""
Chart utility functions for generating Plotly visual indicators.
"""
import plotly.express as px
import pandas as pd

# Career-themed colors matching configuration setup
THEME_PRIMARY = "#1E3A8A"   # Professional Blue
THEME_SECONDARY = "#10B981" # Emerald Green

def create_problems_by_topic_chart(df: pd.DataFrame):
    """
    Creates a Plotly Express bar chart showing the sum of problems solved by topic.

    Args:
        df (pd.DataFrame): Screened candidate data.

    Returns:
        plotly.graph_objects.Figure: Bar chart figure.
    """
    if df is None or df.empty:
        return None
        
    # Aggregate data by Topic
    aggregated = df.groupby("Topic", as_index=False)["ProblemsSolved"].sum()
    
    fig = px.bar(
        aggregated,
        x="Topic",
        y="ProblemsSolved",
        title="📚 Problems Solved by Topic",
        labels={"ProblemsSolved": "Problems Solved", "Topic": "Topic"},
        color_discrete_sequence=[THEME_PRIMARY]
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_mock_score_trend_chart(df: pd.DataFrame):
    """
    Creates a Plotly Express line chart showing the average Mock Score per Date.

    Args:
        df (pd.DataFrame): Screened candidate data.

    Returns:
        plotly.graph_objects.Figure: Line chart figure.
    """
    if df is None or df.empty:
        return None
        
    # Aggregate data by Date (average MockScore per Date)
    aggregated = df.groupby("Date", as_index=False)["MockScore"].mean()
    
    fig = px.line(
        aggregated,
        x="Date",
        y="MockScore",
        title="📈 Mock Score Trend (Average %)",
        labels={"MockScore": "Avg Mock Score (%)", "Date": "Date"},
        markers=True,
        color_discrete_sequence=[THEME_SECONDARY]
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def create_application_trend_chart(df: pd.DataFrame):
    """
    Creates a Plotly Express line chart showing the total Applications sent per Date.

    Args:
        df (pd.DataFrame): Screened candidate data.

    Returns:
        plotly.graph_objects.Figure: Line chart figure.
    """
    if df is None or df.empty:
        return None
        
    # Aggregate data by Date (total Applications per Date)
    aggregated = df.groupby("Date", as_index=False)["Applications"].sum()
    
    fig = px.line(
        aggregated,
        x="Date",
        y="Applications",
        title="💼 Applications Sent Trend",
        labels={"Applications": "Total Applications", "Date": "Date"},
        markers=True,
        color_discrete_sequence=[THEME_PRIMARY]
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
