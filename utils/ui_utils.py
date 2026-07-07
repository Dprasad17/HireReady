"""
Reusable UI component helpers for rendering uniform footers, empty states, and branding.
"""
import streamlit as st
import os

def render_page_header(title: str, description: str):
    """
    Renders a consistent page title, subtitle, and injects professional global CSS styling.

    Args:
        title (str): Title text with emoji prefix.
        description (str): Subtitle description text.
    """
    # Professional Custom CSS overrides for a premium, sleek workspace look
    st.markdown(
        """
        <style>
            /* Import Premium Font */
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
            
            /* Apply typography globally */
            html, body, [class*="css"], .stMarkdown, p, div, label {
                font-family: 'Outfit', sans-serif !important;
            }
            
            /* Modern Card Styling for Streamlit metrics */
            [data-testid="stMetricValue"] {
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                background: linear-gradient(135deg, #38BDF8, #818CF8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 0.9rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.05em !important;
                color: #94A3B8 !important;
            }
            
            [data-testid="metric-container"] {
                background: rgba(30, 41, 59, 0.5) !important;
                border: 1px solid rgba(255, 255, 255, 0.05) !important;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
                border-radius: 12px !important;
                padding: 18px 24px !important;
                transition: transform 0.3s ease, border-color 0.3s ease !important;
            }
            
            [data-testid="metric-container"]:hover {
                transform: translateY(-4px) !important;
                border-color: rgba(99, 102, 241, 0.4) !important;
            }
            
            /* Styling buttons for a modern touch */
            .stButton>button {
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: all 0.2s ease-in-out !important;
                background: linear-gradient(135deg, #4F46E5, #3B82F6) !important;
                color: white !important;
                border: none !important;
                padding: 8px 16px !important;
            }
            
            .stButton>button:hover {
                background: linear-gradient(135deg, #6366F1, #60A5FA) !important;
                box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
                transform: scale(1.02) !important;
            }
            
            /* Glassmorphism sidebar elements */
            section[data-testid="stSidebar"] {
                background-color: #0F172A !important;
                border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
            }
            
            /* Clean divider lines */
            hr {
                border: 0 !important;
                height: 1px !important;
                background: linear-gradient(to right, rgba(255, 255, 255, 0.01), rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.01)) !important;
                margin: 2rem 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Styled header layout
    st.markdown(
        f"""
        <div style="margin-bottom: 25px;">
            <h1 style="font-size: 2.5rem; font-weight: 700; background: linear-gradient(to right, #F8FAFC, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
            <p style="color: #94A3B8; font-size: 1.1rem; margin-top: -5px;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

def render_logo(sidebar: bool = False):
    """
    Displays the HireReady logo if available in the assets folder.

    Args:
        sidebar (bool): True if rendering inside the sidebar container.
    """
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        if sidebar:
            # Render a smaller logo at the top of the sidebar
            st.sidebar.image(logo_path, width="stretch")
            st.sidebar.markdown(
                "<h3 style='text-align: center; color: #1E3A8A; margin-top: -10px;'>HireReady</h3>",
                unsafe_allow_html=True
            )
            st.sidebar.markdown("---")
        else:
            # Render logo on main pages
            st.image(logo_path, width=120)
    else:
        if sidebar:
            st.sidebar.markdown("### 💼 HireReady")
            st.sidebar.markdown("---")

def render_empty_state(message: str, suggestions: list | None = None):
    """
    Renders a standardized professional empty state panel with icons and helpful suggestions.

    Args:
        message (str): Custom description of the missing state.
        suggestions (list): Bullet items suggesting how to resolve the empty state.
    """
    st.warning(f"⚠️ **Notice**: {message}")
    if suggestions:
        st.info(
            "💡 **Action Recommended**:\n" +
            "\n".join([f"- {item}" for item in suggestions])
        )

def render_footer():
    """
    Renders a unified footer section across all multipage endpoints.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #9CA3AF; font-size: 0.85em; padding-top: 15px;'>
            <strong>HireReady</strong> | Placement Readiness Intelligence Dashboard<br>
            <span style='font-size: 0.9em;'>Built using: Streamlit • Pandas • Plotly • Folium</span>
        </div>
        """,
        unsafe_allow_html=True
    )

